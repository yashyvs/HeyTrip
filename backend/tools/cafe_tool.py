def get_cafes(city):

    cafes={

        "Delhi":[

            "Cafe Delhi Heights",

            "Diggin Cafe",

            "Hauz Khas Social",

            "32nd Avenue"
        ]
    }

    return cafes.get(
        city,
        []
    )