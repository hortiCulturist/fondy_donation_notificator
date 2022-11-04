import datetime
import json

import aiohttp
from fastapi import FastAPI, Request
import uvicorn
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

app = FastAPI()


@app.post('/fondy_donation')
async def new_donation_info(request: Request):
    payment_data = await request.json()
    amount = round(int(payment_data['amount']) / 100, 2)
    merchant_data = json.loads(payment_data['merchant_data'])
    user_name = merchant_data[0]['value']
    comment_text = merchant_data[1]['value']
    order_date_time = datetime.datetime.strptime(payment_data['order_time'], '%d.%m.%Y %H:%M:%S')

    notification_text = f'<b>🍩 {user_name}: {amount} грн.</b>%0A' \
                        f'Коментар: {comment_text}%0A' \
                        f'{order_date_time.hour}:{order_date_time.minute}'

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.telegram.org/bot5507237803:AAF6GdYatEaDR1LWpQNRLW_R2w9K7kWjXTI/'
                               f'sendMessage?chat_id=-1001728843948&text={notification_text}&parse_mode=HTML') as resp:
            return JSONResponse(
                status_code=resp.status,
                content=jsonable_encoder({"body": resp.status}),
            )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
