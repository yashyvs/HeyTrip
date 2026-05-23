def get_historical_places(city):

    places = {

        "Delhi":[
            "Red Fort",
            "Humayun Tomb",
            "Qutub Minar",
            "Jama Masjid"
        ],

        "Agra":[
            "Taj Mahal",
            "Agra Fort"
        ]
    }

    return places.get(
        city,
        []
    )