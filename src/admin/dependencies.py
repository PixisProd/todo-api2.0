from typing import Annotated

from fastapi import Depends

from src.admin.service import verify_admin


admin_dependency = Annotated[dict, Depends(verify_admin)]
