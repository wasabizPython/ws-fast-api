from decouple import config

authorization = {
    "user": "user123#"
}

resourceAccess = {
    "user": [
        f"http://127.0.0.1:5000{config('API_PREFIX')}/user/get",
        f"http://127.0.0.1:5000{config('API_PREFIX')}/user/add",
        f"http://127.0.0.1:5000{config('API_PREFIX')}/coin/get"
    ]
}
