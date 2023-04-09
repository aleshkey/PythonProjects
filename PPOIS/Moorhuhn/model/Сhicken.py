class Chicken:
    x = 0
    y = 0

    is_dying = False

    mode = 1

    counter = 0

    flight_images = [
        'images/chicken_flight/chicken1.png',
        'images/chicken_flight/chicken2.png',
        'images/chicken_flight/chicken3.png',
        'images/chicken_flight/chicken4.png',
        'images/chicken_flight/chicken5.png',
        'images/chicken_flight/chicken6.png',
        'images/chicken_flight/chicken7.png',
        'images/chicken_flight/chicken8.png',
        'images/chicken_flight/chicken9.png',
        'images/chicken_flight/chicken10.png',
        'images/chicken_flight/chicken11.png',
        'images/chicken_flight/chicken12.png'
    ]

    death_images = [
        'images/chicken_flight_death/chickendead1.png',
        'images/chicken_flight_death/chickendead2.png',
        'images/chicken_flight_death/chickendead3.png',
        'images/chicken_flight_death/chickendead4.png',
        'images/chicken_flight_death/chickendead5.png',
        'images/chicken_flight_death/chickendead6.png',
        'images/chicken_flight_death/chickendead7.png',
        'images/chicken_flight_death/chickendead8.png'
    ]

    def get_image(self):
        if not self.is_dying:
            if self.counter > 10:
                self.counter = -1
            self.counter += 1
            return self.flight_images[self.counter]
        else:
            return self.get_death_image()

    def get_death_image(self):
        self.counter += 1
        return self.death_images[self.counter]
