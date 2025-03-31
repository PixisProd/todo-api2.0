from typing import Annotated

from fastapi import Depends

from src.auth.service import verify_access_token


user_dependency = Annotated[dict, Depends(verify_access_token)]