import json
import os

import firebase_admin
from firebase_admin import credentials, firestore


_firestore_client = None


def _initialize_firebase():
    global _firestore_client
    if _firestore_client is not None:
        return _firestore_client

    credential_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    credential_json = os.getenv("FIREBASE_CREDENTIALS_JSON")

    if not credential_path and not credential_json:
        return None

    if not firebase_admin._apps:
        if credential_path:
            cred = credentials.Certificate(credential_path)
        else:
            parsed = json.loads(credential_json)
            cred = credentials.Certificate(parsed)
        firebase_admin.initialize_app(cred)

    _firestore_client = firestore.client()
    return _firestore_client


def save_chat_record(user, user_message, bot_reply, source):
    db = _initialize_firebase()
    if db is None:
        return False

    db.collection("chat_history").add(
        {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "user_message": user_message,
            "bot_reply": bot_reply,
            "source": source,
            "created_at": firestore.SERVER_TIMESTAMP,
        }
    )
    return True
