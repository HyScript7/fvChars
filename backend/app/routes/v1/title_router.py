from fastapi import APIRouter, Depends, HTTPException, status

from ...database import Session, get_db
from ...errors.title_errors import DuplicateTitleValueException
from ...middleware.sessions import UserSession, get_user_session
from ...models import TitleModel
from ...schemas import default_schema, title_schema
from ...services import title_service

router: APIRouter = APIRouter()


@router.post(
    "/create",
    response_model=title_schema.TitleResponse,
    responses={401: {"model": default_schema.GenericHTTPException}},
)
async def create(
    title_body: title_schema.TitleCreate,
    db: Session = Depends(get_db),
    session: UserSession = Depends(get_user_session),
):
    if session.is_guest:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must provide a token to create titles!",
        )
    try:
        title = title_service.create_title(db, session.user, title_body.title)
    except DuplicateTitleValueException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate title already exists!",
        )
    return title


@router.get(
    "/own",
    response_model=list[title_schema.TitleResponse],
    responses={401: {"model": default_schema.GenericHTTPException}},
)
async def get_own(
    db: Session = Depends(get_db), session: UserSession = Depends(get_user_session)
):
    if session.is_guest:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must provide a token to view titles!",
        )
    titles = title_service.get_titles(db, session.user)
    return titles
