from drafter import *
from dataclasses import dataclass


# Categories that users can browse
CATEGORIES = [
    "All Types",
    "Sports",
    "JDM",
    "Muscle",
    "Luxury",
    "Supercars"
]


# Stores information about one car
@dataclass
class Car:
    brand: str
    model: str
    category: str
    price: float
    horsepower: int


# Stores information that the website needs to remember
@dataclass
class State:
    garage: list[Car]
    selected_category: str
    search_query: str
    message: str
    available_cars: list[Car]


# HOME PAGE
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("DREAM GARAGE"),
        "Build your dream car collection!",
        "",
        state.message,
        "",
        "Welcome to Dream Garage. Browse cars, add your favorites,",
        "and create your own virtual collection.",
        "",
        Button("Explore Cars", "explore"),
        Button("View My Garage", "garage")
    ])


# EXPLORE CARS PAGE
@route
def explore(state: State) -> Page:
    return Page(state, [
        Header("Explore Cars"),
        "Browse the available cars or search for a specific vehicle.",
        "",
        "Choose a category:",
        SelectBox(
            "choice",
            CATEGORIES,
            state.selected_category
        ),
        Button("View Category", "category"),
        "",
        "Search for a car:",
        TextBox("query", state.search_query),
        Button("Search", "search_cars"),
        "",
        Button("Back Home", "index")
    ])


# CATEGORY PAGE
@route
def category(state: State, choice: str) -> Page:
    state.selected_category = choice

    content = [
        Header(state.selected_category + " Cars"),
        "Here are the cars in this category:",
        ""
    ]

    found_car = False

    for i in range(len(state.available_cars)):
        car = state.available_cars[i]

        if (state.selected_category == "All Types"
                or car.category == state.selected_category):
            found_car = True
            content.append(
                car.brand + " " + car.model
            )
            content.append(
                "Category: " + car.category
            )
            content.append(
                "Price: $" + format(car.price, ",.0f")
            )
            content.append(
                Button(
                    "View Details",
                    "car_details",
                    [Argument("car_index", i)]
                )
            )
            content.append("")

    if not found_car:
        content.append("There are no cars in this category yet.")

    content.append(Button("Back to Explore", "explore"))
    content.append(Button("My Garage", "garage"))

    return Page(state, content)


# CAR DETAILS PAGE
@route
def car_details(state: State, car_index: int) -> Page:
    if car_index < 0 or car_index >= len(state.available_cars):
        state.message = "That car could not be found."
        return explore(state)

    car = state.available_cars[car_index]

    return Page(state, [
        Header(car.brand + " " + car.model),
        "Category: " + car.category,
        "Price: $" + format(car.price, ",.0f"),
        "Horsepower: " + str(car.horsepower) + " HP",
        "",
        Button(
            "Add to My Garage",
            "add_to_garage",
            [Argument("car_index", car_index)]
        ),
        Button("Back to Explore", "explore"),
        Button("View My Garage", "garage")
    ])


# ADD AN EXISTING CAR TO THE GARAGE
@route
def add_to_garage(state: State, car_index: int) -> Page:
    if 0 <= car_index < len(state.available_cars):
        car = state.available_cars[car_index]

        new_car = Car(
            car.brand,
            car.model,
            car.category,
            car.price,
            car.horsepower
        )

        state.garage.append(new_car)
        state.message = (
            car.brand + " " + car.model + " was added to your garage!"
        )
    else:
        state.message = "That car could not be added."

    return garage(state)


# SEARCH FOR CARS
@route
def search_cars(state: State, query: str) -> Page:
    state.search_query = query

    content = [
        Header("Search Results"),
        "Search: " + state.search_query,
        ""
    ]

    found_car = False
    search_text = query.lower()

    for i in range(len(state.available_cars)):
        car = state.available_cars[i]

        if (search_text in car.brand.lower()
                or search_text in car.model.lower()
                or search_text in car.category.lower()):
            found_car = True

            content.append(car.brand + " " + car.model)
            content.append(
                "Category: " + car.category
            )
            content.append(
                "Price: $" + format(car.price, ",.0f")
            )
            content.append(
                Button(
                    "View Details",
                    "car_details",
                    [Argument("car_index", i)]
                )
            )
            content.append("")

    if not found_car:
        content.append("No cars matched your search.")

    content.append(Button("Search Again", "explore"))
    content.append(Button("Back Home", "index"))

    return Page(state, content)


# MY GARAGE PAGE
@route
def garage(state: State) -> Page:
    content = [
        Header("My Garage"),
        state.message,
        ""
    ]

    total_value = 0.0

    if len(state.garage) == 0:
        content.append("Your garage is currently empty.")
        content.append("Explore cars to start your collection.")
    else:
        content.append("Your current car collection:")
        content.append("")

        for i in range(len(state.garage)):
            car = state.garage[i]

            content.append(
                car.brand + " " + car.model
            )
            content.append(
                "Category: " + car.category
            )
            content.append(
                "Price: $" + format(car.price, ",.0f")
            )
            content.append(
                "Horsepower: " + str(car.horsepower) + " HP"
            )
            content.append(
                Button(
                    "Remove This Car",
                    "remove_car",
                    [Argument("car_index", i)]
                )
            )
            content.append("")

            total_value = total_value + car.price

    content.append(
        "Total Collection Value: $"
        + format(total_value, ",.0f")
    )
    content.append("")
    content.append(Button("Explore Cars", "explore"))
    content.append(Button("Add a Custom Car", "add_custom_car"))
    content.append(Button("Clear My Garage", "clear_garage"))
    content.append(Button("Home", "index"))

    return Page(state, content)


# ADD CUSTOM CAR PAGE
@route
def add_custom_car(state: State) -> Page:
    return Page(state, [
        Header("Add a Custom Car"),
        "Enter the information for your own car.",
        "",
        "Brand:",
        TextBox("brand"),
        "",
        "Model:",
        TextBox("model"),
        "",
        "Category:",
        SelectBox(
            "custom_category",
            CATEGORIES[1:],
            "Sports"
        ),
        "",
        "Price:",
        TextBox("price"),
        "",
        "Horsepower:",
        TextBox("horsepower"),
        "",
        Button("Add Car to Garage", "save_custom_car"),
        Button("Back to Garage", "garage")
    ])


# SAVE A CUSTOM CAR
@route
def save_custom_car(
        state: State,
        brand: str,
        model: str,
        custom_category: str,
        price: float,
        horsepower: int
) -> Page:

    if brand.strip() == "" or model.strip() == "":
        state.message = "Please enter both a brand and model."
        return add_custom_car(state)

    if price < 0 or horsepower < 0:
        state.message = "Price and horsepower cannot be negative."
        return add_custom_car(state)

    new_car = Car(
        brand.strip(),
        model.strip(),
        custom_category,
        price,
        horsepower
    )

    state.garage.append(new_car)
    state.message = (
        brand + " " + model + " was added to your garage!"
    )

    return garage(state)


# REMOVE A CAR FROM THE GARAGE
@route
def remove_car(state: State, car_index: int) -> Page:
    if 0 <= car_index < len(state.garage):
        removed_car = state.garage.pop(car_index)

        state.message = (
            removed_car.brand + " " + removed_car.model
            + " was removed from your garage."
        )
    else:
        state.message = "That car could not be removed."

    return garage(state)


# CLEAR THE GARAGE
@route
def clear_garage(state: State) -> Page:
    state.garage.clear()
    state.message = "Your garage has been cleared."

    return garage(state)


# START THE WEBSITE
start_server(State(
    garage=[],
    selected_category="All Types",
    search_query="",
    message="Welcome to Dream Garage!",
    available_cars=[
        Car("Nissan", "GT-R R35", "JDM", 120000, 565),
        Car("Toyota", "Supra MK5", "JDM", 60000, 382),
        Car("Honda", "Civic Type R", "JDM", 46000, 315),
        Car("Ford", "Mustang GT", "Muscle", 45000, 480),
        Car("Chevrolet", "Camaro SS", "Muscle", 48000, 455),
        Car("Dodge", "Challenger Hellcat", "Muscle", 85000, 717),
        Car("Porsche", "911 Carrera", "Sports", 120000, 388),
        Car("Chevrolet", "Corvette C8", "Sports", 75000, 495),
        Car("BMW", "M4 Competition", "Luxury", 85000, 523),
        Car("Mercedes-Benz", "AMG GT", "Luxury", 110000, 523),
        Car("Ferrari", "488 GTB", "Supercars", 250000, 660),
        Car("Lamborghini", "Huracan", "Supercars", 280000, 631)
    ]
))
