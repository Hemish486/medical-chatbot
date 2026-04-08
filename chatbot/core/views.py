from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils import timezone
from urllib.parse import urljoin
from openai import OpenAI
from datetime import timedelta
import csv
import io
import os
import re
import requests
import math
from django.conf import settings
from django.core.mail import send_mail

from .firebase_utils import save_chat_record
from .forms import SignUpForm
from .models import ChatHistory, UserProfile

api_key = (
    os.getenv("OPENAI_API_KEY")
    or os.getenv("OPENAI_KEY")
    or os.getenv("GITHUB_TOKEN")
    or os.getenv("GITHUB_PAT")
)
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
github_model = os.getenv("GITHUB_MODEL", "openai/gpt-4o-mini")
github_models_base_url = os.getenv("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference")
api_only_mode = os.getenv("API_ONLY_MODE", "true").strip().lower() in {"1", "true", "yes", "on"}
CHAT_ALLOWED_ROLES = {"patient", "doctor"}
ADMIN_ROLE = "admin"
CHAT_HISTORY_RETENTION_DAYS = int(os.getenv("CHAT_HISTORY_RETENTION_DAYS", "90"))
PRIVACY_NOTICE_TEXT = (
    "This application stores chat history to help users review prior conversations. "
    "Medical information entered here should be limited to what is needed for the support request. "
    "Do not enter highly sensitive details unless required. The chatbot is not for emergencies or diagnosis."
)


def render_main_page(request, profile, role, privacy_accepted=True):
    return render(
        request,
        'main.html',
        {
            'email_verified': profile.email_verified,
            'can_use_chat': role in CHAT_ALLOWED_ROLES,
            'role': role,
            'privacy_accepted': privacy_accepted,
            'privacy_notice_text': PRIVACY_NOTICE_TEXT,
            'retention_days': CHAT_HISTORY_RETENTION_DAYS,
        },
    )


def get_retention_cutoff():
    if CHAT_HISTORY_RETENTION_DAYS <= 0:
        return None
    return timezone.now() - timedelta(days=CHAT_HISTORY_RETENTION_DAYS)


def purge_expired_chat_history():
    cutoff = get_retention_cutoff()
    if cutoff is not None:
        ChatHistory.objects.filter(created_at__lt=cutoff).delete()


def mask_sensitive_text(text):
    if not text:
        return text

    masked = text
    masked = re.sub(r"[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}", "[email removed]", masked)
    masked = re.sub(r"(?:(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4})", "[phone removed]", masked)
    masked = re.sub(r"\b\d{5,}\b", "[number removed]", masked)
    return masked.strip()


def save_minimized_chat_record(user, user_input, bot_reply, source):
    ChatHistory.objects.create(
        user=user,
        user_message=mask_sensitive_text(user_input),
        bot_reply=bot_reply,
        source=source or "",
    )

def normalize_github_base_url(url):
    if not isinstance(url, str) or not url.strip():
        return "https://models.github.ai/inference"
    normalized = url.strip().rstrip("/")
    return normalized

def is_github_pat(value):
    return isinstance(value, str) and value.strip().startswith("github_pat_")

def looks_like_openai_key(value):
    if not isinstance(value, str):
        return False
    token = value.strip()
    return token.startswith("sk-") or token.startswith("sess-")

def looks_like_supported_api_key(value):
    return is_github_pat(value) or looks_like_openai_key(value)

def generate_ai_response_text(user_input, key):
    # Use GitHub Models API flow when token is a GitHub PAT.
    if is_github_pat(key):
        base_url = normalize_github_base_url(github_models_base_url)
        endpoint = f"{base_url}/chat/completions"
        model_candidates = [
            github_model,
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini",
            "openai/gpt-4o-mini",
        ]
        seen = set()
        deduped_candidates = []
        for candidate in model_candidates:
            if candidate and candidate not in seen:
                seen.add(candidate)
                deduped_candidates.append(candidate)

        # Try model fallbacks if a specific model is unavailable.
        last_error = None
        for candidate in deduped_candidates:
            try:
                response = requests.post(
                    endpoint,
                    headers={
                        "Authorization": f"Bearer {key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": candidate,
                        "messages": [{"role": "user", "content": user_input}],
                        "max_tokens": 400,
                    },
                    timeout=30,
                )
                if response.status_code >= 400:
                    raise Exception(f"Error code: {response.status_code} - {response.text}")
                data = response.json()
                choices = data.get("choices", [])
                if choices and choices[0].get("message"):
                    return choices[0]["message"].get("content", "") or ""
                return ""
            except Exception as e:
                last_error = e
                error_text = str(e).lower()
                if "unknown_model" in error_text or "unknown model" in error_text:
                    continue
                raise

        if last_error is not None:
            raise last_error
        return ""

    response = OpenAI(api_key=key).responses.create(
        model=openai_model,
        input=user_input,
    )
    return response.output_text

def with_dev_source_tag(message, source):
    if settings.DEBUG and source in {"API", "OFFLINE", "API_ERROR"}:
        return f"[{source}] {message}"
    return message

# English medical keywords (simple substring match)
MEDICAL_KEYWORDS = [
    # General medical query phrases (English)
    'remedy', 'remedies', 'cure', 'treat', 'treatment', 'how to', 'what to do',
    'home remedy', 'medicine for', 'tablet for', 'drug for', 'relief from',
    'cause of', 'causes of', 'symptoms of', 'sign of', 'prevent', 'prevention',
    # English symptoms & conditions
    'fever', 'vomit', 'vomiting', 'nausea', 'diarrhea', 'diarrhoea', 'headache',
    'cough', 'cold', 'flu', 'pain', 'ache', 'sore', 'infection', 'allergy',
    'rash', 'swelling', 'bleeding', 'fracture', 'injury', 'wound', 'burn',
    'dizzy', 'dizziness', 'fatigue', 'tired', 'weakness', 'breathless',
    'chest pain', 'heart', 'blood pressure', 'diabetes', 'asthma', 'cancer',
    'stroke', 'seizure', 'anxiety', 'depression', 'insomnia', 'migraine',
    'stomach', 'back pain', 'knee', 'joint', 'muscle', 'bone', 'skin',
    'throat', 'ear', 'eye', 'nose', 'lung', 'liver', 'kidney', 'brain',
    'doctor', 'hospital', 'medicine', 'drug', 'tablet', 'prescription',
    'symptom', 'diagnosis', 'treatment', 'surgery', 'vaccine', 'therapy',
    'antibiotic', 'painkiller', 'fever', 'temperature', 'pulse', 'blood',
    'urine', 'test', 'scan', 'xray', 'mri', 'ultrasound', 'ecg',
    'pregnant', 'pregnancy', 'period', 'menstrual', 'cholesterol',
    'dehydration', 'constipation', 'bloating', 'acid reflux', 'ulcer',
    'covid', 'coronavirus', 'monkeypox', 'malaria', 'typhoid', 'dengue',
    'tuberculosis', 'hiv', 'aids', 'hepatitis', 'pneumonia', 'bronchitis',
    'appendix', 'gallstone', 'kidney stone', 'hernia', 'arthritis',
    'osteoporosis', 'thyroid', 'anemia', 'leukemia', 'lymphoma',
    'hair fall', 'hair loss', 'alopecia', 'balding', 'thinning hair',
    'overdose', 'poisoning', 'allerg', 'immune', 'vitamin', 'supplement',
    'health', 'medical', 'clinic', 'pharmacy', 'nurse', 'surgeon',
]

def is_medical_query(user_input):
    text = user_input.lower()
    return any(keyword.lower() in text for keyword in MEDICAL_KEYWORDS)

def geocode_location(location_text):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_text,
        "format": "json",
        "limit": 1,
    }
    headers = {"User-Agent": "medical-chatbot/1.0"}
    response = requests.get(url, params=params, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    if not data:
        return None

    place = data[0]
    return {
        "name": place.get("display_name", location_text),
        "lat": float(place["lat"]),
        "lon": float(place["lon"]),
    }

def haversine_km(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return earth_radius_km * 2 * math.asin(math.sqrt(a))

def find_nearby_healthcare(lat, lon, radius_km=50, limit=8):
    radius_m = int(radius_km * 1000)
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node[\"amenity\"=\"hospital\"](around:{radius_m},{lat},{lon});
      node[\"amenity\"=\"clinic\"](around:{radius_m},{lat},{lon});
      node[\"amenity\"=\"doctors\"](around:{radius_m},{lat},{lon});
      way[\"amenity\"=\"hospital\"](around:{radius_m},{lat},{lon});
      way[\"amenity\"=\"clinic\"](around:{radius_m},{lat},{lon});
      way[\"amenity\"=\"doctors\"](around:{radius_m},{lat},{lon});
    );
    out center tags;
    """

    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=overpass_query,
        timeout=30,
    )
    response.raise_for_status()
    elements = response.json().get("elements", [])

    facilities = []
    for element in elements:
        tags = element.get("tags", {})
        if "lat" in element and "lon" in element:
            element_lat = float(element["lat"])
            element_lon = float(element["lon"])
        else:
            center = element.get("center")
            if not center:
                continue
            element_lat = float(center["lat"])
            element_lon = float(center["lon"])

        distance = haversine_km(lat, lon, element_lat, element_lon)
        address_parts = [
            tags.get("addr:street", "").strip(),
            tags.get("addr:housenumber", "").strip(),
            tags.get("addr:city", "").strip(),
        ]
        address = " ".join(part for part in address_parts if part).strip()
        facilities.append(
            {
                "name": tags.get("name", "Unnamed healthcare facility"),
                "type": tags.get("amenity", "healthcare"),
                "address": address,
                "distance_km": round(distance, 1),
            }
        )

    facilities.sort(key=lambda facility: facility["distance_km"])
    return facilities[:limit]

def format_nearby_facilities(location_name, facilities):
    if not facilities:
        return (
            f"I couldn't find clinics or hospitals within 50 km of {location_name}. "
            "Please try a nearby city/town name or a more specific location."
        )

    lines = [f"Nearby clinics/hospitals within 50 km of {location_name}:"]
    for index, facility in enumerate(facilities, start=1):
        type_label = facility["type"].capitalize()
        address = facility["address"] if facility["address"] else "Address not available"
        lines.append(
            f"{index}. {facility['name']}"
        )
        lines.append(
            f"   Type: {type_label} | Distance: {facility['distance_km']} km"
        )
        lines.append(
            f"   Address: {address}"
        )
    lines.append("Please go to one of the listed clinics/hospitals if symptoms are worsening.")
    lines.append("If symptoms are severe, seek emergency care immediately.")
    return "\n".join(lines)

def is_doctor_lookup_intent(user_input):
    text = user_input.lower().strip()
    intent_terms = [
        'doctor', 'doctors', 'clinic', 'hospital', 'nearby', 'near me', 'find doctor',
        'find hospital', 'show hospitals', 'show clinics', 'locate', 'location',
        'nearby hospital', 'nearby clinic', 'nearest', 'book doctor'
    ]
    return any(term in text for term in intent_terms)

def is_affirmative(user_input):
    text = user_input.lower().strip()
    affirm_terms = [
        'yes', 'y', 'yeah', 'yep', 'sure', 'ok', 'okay', 'please'
    ]
    return text in affirm_terms or any(text.startswith(term) for term in ['yes '])

def offline_medical_response(user_input):
    text = user_input.lower()

    has_fever = any(term in text for term in ['fever', 'temperature'])
    has_vomiting = any(term in text for term in ['vomit', 'vomiting', 'nausea'])
    has_diarrhea = any(term in text for term in ['diarrhea', 'diarrhoea'])
    has_hair_fall = any(term in text for term in ['hair fall', 'hair loss', 'alopecia', 'balding', 'thinning hair'])

    treatment_intent_terms = [
        'remedy', 'remedies', 'how to treat', 'treat', 'treatment', 'medicine for',
        'what to take', 'what should i take', 'home remedy', 'relief for'
    ]

    if any(term in text for term in treatment_intent_terms):
        return (
            "General treatment guide (not a diagnosis): 1) Rest and hydrate well. "
            "2) Use only standard OTC medicines suitable for your age/conditions. "
            "3) Avoid antibiotics unless prescribed. 4) Monitor red flags: breathing trouble, "
            "chest pain, confusion, persistent high fever, blood in vomit/stool, severe dehydration. "
            "If any red flag appears, seek urgent care. "
            "Share your symptoms, duration, age, and current medicines for a more specific safe suggestion."
        )

    if has_fever and has_vomiting:
        return (
            "For fever with vomiting: prioritize hydration (ORS/water in small frequent sips), rest, and light food. "
            "Paracetamol/acetaminophen may help fever if appropriate for you. "
            "Seek urgent care if there is persistent vomiting, inability to keep fluids down, blood in vomit, "
            "severe weakness, confusion, breathing issues, or very high fever."
        )

    if has_fever:
        return (
            "For fever: rest, drink plenty of fluids, and use paracetamol/acetaminophen if appropriate. "
            "Seek urgent care if fever is very high, lasts more than 3 days, or includes breathing issues/confusion."
        )
    if has_vomiting:
        return (
            "For vomiting/nausea: sip oral rehydration fluids, eat light food, and avoid oily/spicy meals. "
            "Go to a doctor if vomiting is persistent, contains blood, or causes dehydration."
        )
    if has_diarrhea:
        return (
            "For diarrhea: use oral rehydration solution, avoid heavy/fatty food, and monitor hydration. "
            "Seek medical help if it lasts more than 2 days, there is blood, or severe weakness appears."
        )
    if has_hair_fall:
        return (
            "For hair fall: common causes include stress, poor nutrition, thyroid/iron/vitamin issues, hormonal changes, "
            "or scalp conditions. Use gentle hair care and ensure enough protein, iron, vitamin D, and B12 in diet. "
            "If shedding is heavy, patchy, or lasts more than 6-8 weeks, consult a dermatologist for tests and targeted treatment."
        )

    return (
        "I can provide general medical information, but this is not a diagnosis. "
        "Please share your symptoms (duration, severity, age, existing conditions, medicines) for safer guidance."
    )


def resolve_user_role(user, profile=None):
    # Admin can be a superuser or a user in the admin group.
    if user.is_superuser or user.groups.filter(name=ADMIN_ROLE).exists():
        return ADMIN_ROLE
    if profile is None:
        profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile.role


def build_verification_url(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verify_path = reverse("verify_email", kwargs={"uidb64": uid, "token": token})
    public_base_url = (os.getenv("PUBLIC_BASE_URL") or "").strip().rstrip("/")
    if public_base_url:
        return urljoin(f"{public_base_url}/", verify_path.lstrip("/"))
    return request.build_absolute_uri(verify_path)


def send_verification_email(request, user):
    verification_url = build_verification_url(request, user)
    subject = "Verify your email"
    message = render_to_string(
        "registration/verification_email.txt",
        {
            "user": user,
            "verification_url": verification_url,
        },
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return verification_url


def privacy_notice_view(request):
    return render(
        request,
        "privacy_notice.html",
        {
            "retention_days": CHAT_HISTORY_RETENTION_DAYS,
            "privacy_notice_text": PRIVACY_NOTICE_TEXT,
        },
    )

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("chatbot")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get("role", "patient")
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.email_verified = False
            profile.save()

            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            try:
                verification_url = send_verification_email(request, user)
            except Exception as exc:
                verification_url = build_verification_url(request, user)
                messages.warning(
                    request,
                    f"Account created, but verification email could not be sent: {exc}.",
                )
                messages.info(request, f"Use this verification link now: {verification_url}")

            messages.success(
                request,
                f"Account created. Verification email sent to {user.email}. Please verify before using the chatbot.",
            )
            if settings.DEBUG:
                messages.info(request, f"Verification link (dev): {verification_url}")
            return redirect("login")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.email_verified = True
        profile.save()
        messages.success(request, "Email verified successfully. You can now use the chatbot.")
        return redirect("chatbot")

    messages.error(request, "Verification link is invalid or expired.")
    return redirect("login")


@login_required
def export_chat_history_view(request):
    cutoff = get_retention_cutoff()
    queryset = ChatHistory.objects.filter(user=request.user)
    if cutoff is not None:
        queryset = queryset.filter(created_at__gte=cutoff)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["created_at", "source", "user_message", "bot_reply"])
    for item in queryset.order_by("-created_at"):
        writer.writerow([
            item.created_at.isoformat(),
            item.source,
            item.user_message,
            item.bot_reply,
        ])

    response = HttpResponse(buffer.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="chat_history.csv"'
    return response


@login_required
def delete_chat_history_view(request):
    if request.method != "POST":
        return redirect("history")

    ChatHistory.objects.filter(user=request.user).delete()
    messages.success(request, "Your chat history has been deleted.")
    return redirect("history")


@login_required
def resend_verification_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.email_verified:
        messages.info(request, "Your email is already verified.")
        return redirect("chatbot")

    try:
        verification_url = send_verification_email(request, request.user)
        messages.success(request, f"Verification email sent to {request.user.email}. Please check your inbox.")
        if settings.DEBUG:
            messages.info(request, f"Verification link (dev): {verification_url}")
    except Exception as exc:
        verification_url = build_verification_url(request, request.user)
        messages.error(request, f"Could not send verification email: {exc}")
        messages.info(request, f"Use this verification link now: {verification_url}")
    return redirect("chatbot")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


@login_required
def chat_history_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    role = resolve_user_role(request.user, profile)
    if role not in CHAT_ALLOWED_ROLES:
        return JsonResponse({"reply": "Only patient/doctor accounts can view this page."}, status=403)

    purge_expired_chat_history()
    cutoff = get_retention_cutoff()
    history_items = ChatHistory.objects.filter(user=request.user)
    if cutoff is not None:
        history_items = history_items.filter(created_at__gte=cutoff)
    return render(
        request,
        "history.html",
        {
            "history_items": history_items[:100],
            "retention_days": CHAT_HISTORY_RETENTION_DAYS,
            "privacy_notice_url": reverse("privacy_notice"),
        },
    )


@login_required
def admin_chat_history_view(request):
    role = resolve_user_role(request.user)
    if role != ADMIN_ROLE:
        return JsonResponse({"reply": "Only admin can view all chat history."}, status=403)

    purge_expired_chat_history()
    cutoff = get_retention_cutoff()
    history_items = ChatHistory.objects.select_related("user")
    if cutoff is not None:
        history_items = history_items.filter(created_at__gte=cutoff)
    return render(
        request,
        "history_admin.html",
        {
            "history_items": history_items[:200],
            "retention_days": CHAT_HISTORY_RETENTION_DAYS,
        },
    )


@login_required
def chatbot(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    role = resolve_user_role(request.user, profile)
    privacy_accepted = request.session.get("privacy_accepted", False)

    if request.method == "POST" and request.POST.get("accept_privacy"):
        request.session["privacy_accepted"] = True
        messages.success(
            request,
            "Privacy notice accepted. You may now use the chatbot and review your data controls.",
        )
        return redirect("chatbot")

    if not privacy_accepted:
        if request.method == "POST":
            return JsonResponse(
                {"reply": "Please accept the privacy and consent notice before using the chatbot."},
                status=403,
            )
        return render_main_page(request, profile, role, privacy_accepted=False)

    # Only patient and doctor roles are allowed to use chatbot features.
    if role not in CHAT_ALLOWED_ROLES:
        if request.method == 'POST':
            return JsonResponse(
                {"reply": "Chatbot access is allowed only for patient/doctor roles."},
                status=403,
            )
        return render_main_page(request, profile, role)

    # Block chat requests until user verifies email.
    if request.method == 'POST' and not profile.email_verified:
        return JsonResponse(
            {
                "reply": "Please verify your email before using the chatbot. Use the 'Resend verification email' link on this page.",
            },
            status=403,
        )

    if request.method == 'POST':
        user_input = (request.POST.get('user_input') or '').strip()
        if not user_input:
            return JsonResponse({'reply': "Please enter a message."})

        awaiting_location = request.session.get('awaiting_location_for_medical', False)
        pending_doctor_offer = request.session.get('pending_doctor_offer', False)

        # If location is pending, treat this user message as a location.
        if awaiting_location:
            try:
                location_data = geocode_location(user_input)
                if not location_data:
                    return JsonResponse({'reply': (
                        "I couldn't identify that location. Please share a city/area/pincode again "
                        "(example: Pune, 411001, London)."
                    )})

                nearby_facilities = find_nearby_healthcare(
                    location_data['lat'],
                    location_data['lon'],
                    radius_km=50,
                    limit=8,
                )
                response_text = format_nearby_facilities(location_data['name'], nearby_facilities)
            except Exception as e:
                print(f"Location search error: {str(e)}")
                response_text = (
                    "I could not fetch nearby clinics right now. "
                    "Please try again in a moment with city + pincode."
                )

            request.session['awaiting_location_for_medical'] = False
            request.session['pending_doctor_offer'] = False
            return JsonResponse({'reply': response_text})

        # User asked for nearby care; next step is collecting location.
        if pending_doctor_offer and (is_affirmative(user_input) or is_doctor_lookup_intent(user_input)):
            request.session['awaiting_location_for_medical'] = True
            request.session['pending_doctor_offer'] = False
            response_text = (
                "Please share your location (city/area/pincode), and I will list nearby "
                "clinics/hospitals within 50 km."
            )
            return JsonResponse({'reply': response_text})

        if pending_doctor_offer and user_input.lower() in ['no', 'nope', 'not now']:
            request.session['pending_doctor_offer'] = False
            return JsonResponse({'reply': "Okay. If you need nearby doctors later, just type: find doctors near me."})

        if not is_medical_query(user_input):
            return JsonResponse({'reply': "I'm a medical chatbot and can only answer questions related to healthcare. Please ask a medical question."})

        # Use AI if available, otherwise use a safe offline fallback.
        guidance_response = None
        guidance_source = None
        if api_key is not None and not looks_like_supported_api_key(api_key):
            guidance_response = (
                "⚠️ Invalid key format. Use either OPENAI_API_KEY (`sk-...`) "
                "or a GitHub PAT (`github_pat_...`) via GITHUB_TOKEN/OPENAI_API_KEY in .env."
            )
            guidance_source = "API_ERROR"
        elif api_key is not None:
            try:
                guidance_response = generate_ai_response_text(user_input, api_key)
                guidance_source = "API"
            except Exception as e:
                error_msg = str(e)
                if '429' in error_msg or 'insufficient_quota' in error_msg.lower() or 'rate_limit' in error_msg.lower():
                    if api_only_mode:
                        guidance_response = "⚠️ API quota/rate limit reached. This request was not answered via offline fallback because API_ONLY_MODE is enabled."
                        guidance_source = "API_ERROR"
                    else:
                        guidance_response = offline_medical_response(user_input)
                        guidance_source = "OFFLINE"
                elif '401' in error_msg or 'invalid_api_key' in error_msg.lower() or 'authentication' in error_msg.lower():
                    guidance_response = "⚠️ Invalid API key. Check OPENAI_API_KEY (`sk-...`) or GitHub PAT (`github_pat_...`) in .env."
                    guidance_source = "API_ERROR"
                else:
                    if api_only_mode:
                        guidance_response = f"⚠️ API request failed: {error_msg}"
                        guidance_source = "API_ERROR"
                    else:
                        guidance_response = offline_medical_response(user_input)
                        guidance_source = "OFFLINE"
                print(f"OpenAI API error: {error_msg}")
        else:
            if api_only_mode:
                guidance_response = "⚠️ No API key configured. Set OPENAI_API_KEY (`sk-...`) or GITHUB_TOKEN (`github_pat_...`) in .env."
                guidance_source = "API_ERROR"
            else:
                guidance_response = offline_medical_response(user_input)
                guidance_source = "OFFLINE"

        if guidance_response is None:
            if api_only_mode:
                guidance_response = "⚠️ API response was empty."
                guidance_source = "API_ERROR"
            else:
                guidance_response = offline_medical_response(user_input)
                guidance_source = "OFFLINE"

        # Save chat in DB; Firebase mirroring should not break user flow.
        guidance_response = with_dev_source_tag(guidance_response, guidance_source)

        save_minimized_chat_record(
            request.user,
            user_input,
            guidance_response,
            guidance_source or "",
        )
        try:
            save_chat_record(request.user, user_input, guidance_response, guidance_source or "")
        except Exception:
            pass

        request.session['pending_doctor_offer'] = True
        response_text = (
            f"{guidance_response}\n\n"
            "If you want nearby doctors/clinics/hospitals within 50 km, reply with: "
            "find doctors near me"
        )
        return JsonResponse({'reply': response_text})
    purge_expired_chat_history()
    return render_main_page(request, profile, role, privacy_accepted=True)
