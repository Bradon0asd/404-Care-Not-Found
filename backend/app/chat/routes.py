from app.auth.current_user import get_current_user
from app.chat import chat_bp
from app.chat.schemas import (
    BaselineSubmitSchema,
    CareAgentCreateSchema,
    CareAgentSchema,
    ChatMessageCreateSchema,
    ChatMessageSchema,
    ChatRoomCreateSchema,
    ChatRoomSchema,
    ChatTurnSchema,
)
from app.chat.service import (
    baseline_questions,
    create_room,
    get_agent,
    get_room,
    list_rooms,
    process_user_message,
    room_messages,
    save_baseline,
    setup_agent,
)
from app.shared.response import api_success


@chat_bp.get("/chat/agent")
@chat_bp.doc(summary="Read the care agent", security=[{"UserIdHeader": []}])
def get_agent_api():
    agent = get_agent(current_user=get_current_user())
    return api_success(CareAgentSchema().dump(agent))


@chat_bp.post("/chat/agent")
@chat_bp.arguments(CareAgentCreateSchema, location="json")
@chat_bp.doc(summary="Create or update the care agent", security=[{"UserIdHeader": []}])
def setup_agent_api(args):
    agent = setup_agent(current_user=get_current_user(), **args)
    return api_success(CareAgentSchema().dump(agent), status_code=201)


@chat_bp.get("/chat/agent/baseline")
@chat_bp.doc(
    summary="Get the one-off opening questions",
    security=[{"UserIdHeader": []}],
)
def baseline_questions_api():
    questions = baseline_questions(current_user=get_current_user())
    return api_success({"questions": questions})


@chat_bp.post("/chat/agent/baseline")
@chat_bp.arguments(BaselineSubmitSchema, location="json")
@chat_bp.doc(summary="Save the one-off answers", security=[{"UserIdHeader": []}])
def save_baseline_api(args):
    agent = save_baseline(current_user=get_current_user(), answers=args["answers"])
    return api_success(CareAgentSchema().dump(agent))


@chat_bp.get("/chat/rooms")
@chat_bp.doc(summary="List chat rooms", security=[{"UserIdHeader": []}])
def list_rooms_api():
    rooms = list_rooms(current_user=get_current_user())
    return api_success(ChatRoomSchema(many=True).dump(rooms))


@chat_bp.post("/chat/rooms")
@chat_bp.arguments(ChatRoomCreateSchema, location="json")
@chat_bp.doc(summary="Open a chat room", security=[{"UserIdHeader": []}])
def create_room_api(args):
    room = create_room(current_user=get_current_user(), **args)
    return api_success(ChatRoomSchema().dump(room), status_code=201)


@chat_bp.get("/chat/rooms/<int:room_id>")
@chat_bp.doc(summary="Read a chat room with its messages", security=[{"UserIdHeader": []}])
def get_room_api(room_id):
    current_user = get_current_user()
    room = get_room(current_user=current_user, room_id=room_id)
    payload = ChatRoomSchema().dump(room)
    payload["messages"] = ChatMessageSchema(many=True).dump(
        room_messages(current_user=current_user, room_id=room_id)
    )
    return api_success(payload)


@chat_bp.post("/chat/rooms/<int:room_id>/messages")
@chat_bp.arguments(ChatMessageCreateSchema, location="json")
@chat_bp.doc(summary="Send a message and get the reply", security=[{"UserIdHeader": []}])
def send_message_api(args, room_id):
    user_message, ai_message = process_user_message(
        current_user=get_current_user(),
        room_id=room_id,
        text=args["text"],
    )
    return api_success(
        ChatTurnSchema().dump({"user_message": user_message, "ai_message": ai_message}),
        status_code=201,
    )
