def paymentHook(amount , req , tx_ref,  api_key) :
    import requests
    from uuid import uuid4
  
      
    url = "https://api.chapa.co/v1/transaction/initialize"
    payload = {
    "amount": str(amount),
    "currency": "ETB",
    "email": req.user.email,
    "first_name": req.user.first_name,
    "last_name": req.user.last_name,
    
    "tx_ref": tx_ref,
    "callback_url": f"http://localhost:8000/api/verifypayment/?tx_ref={tx_ref}",
   "return_url": "https://vectoredmatrix.vercel.app/",
    }
    headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
    }
      
    response = requests.post(url, json=payload, headers=headers)
    data = response.text
    
    return data