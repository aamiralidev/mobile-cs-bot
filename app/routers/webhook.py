from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()  # await should be used here
    print(data)  # Now data will contain the JSON data sent via POST
    return data  # Send the data back as response
