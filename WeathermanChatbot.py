import time
import pyowm
import re
import sys
import creds

# lines 1-24 are used to test the weather module

# print("Test begin")
# key and initalizer
owm = pyowm.OWM(creds.owm)
mgr = owm.weather_manager()


# runs the main tasks and responses
def main():

    UserInput = keywords(input("YOU: "))
    UserInput = response(UserInput)


# looks through user's input and returns response


def keywords(keyword):
    # creates empty list for keywords
    weatherkeywords = []
    citykeyword = []

    # parameters if user says hello, how are you, or what can you find to the robot
    hellolist = ["hello", "yo", "wsg", "hola", "aloha", "hi", "belo", "bello"]
    greetinglist = ["how are you", "how are you doing"]
    if keyword in hellolist:
        print("BOT: Hello user! What weather information would you like to know?")
        main()
    if keyword in greetinglist:
        print(
            "BOT: Hello user, I am doing great! What weather information would you like to know?"
        )
        main()
    if (
        keyword == "what can you do"
        or keyword == "what can you tell me about"
        or keyword == "what do you know"
    ):
        print(
            "BOT: I am weatherbot, and I can find weather information such as temperature, cloud cover, rainfall, humidity, and wind speed for any city in the world.\nWhat question do you have for me today?"
        )
        main()
        # finds the weather keywords needed
    findkey = keyword.replace(" ", "")
    findkey = findkey.lower()
    # sees if input contains keyword and adds
    # that word to weather list
    if re.search("temp(erature)?.+", findkey):
        weatherkeywords.append("temperature")

    if re.search("cloud(cover)?", findkey):
        weatherkeywords.append("clouds")

    if re.search("humid(ity)?", findkey):
        weatherkeywords.append("humidity")

    if re.search("rain(fall)?", findkey):
        weatherkeywords.append("rain")

    if re.search("wind?.+", findkey):
        weatherkeywords.append("wind")

    if re.search("weather?", findkey):
        weatherkeywords.append("temperature")
        weatherkeywords.append("rain")
        weatherkeywords.append("humidity")
        weatherkeywords.append("wind")
        weatherkeywords.append("clouds")
    if len(weatherkeywords) == 0:
        weatherkeywords.append("none")

        # searches for if valid city

        # puts the cities into a list (oneword cities and two word cities)
    onewordcities = (
        open("citiesoftheworld.txt", "r", encoding="utf8").read().strip().lower()
    )
    citieslist = list(onewordcities.split("\n"))
    twowordcities = (
        open("twonamedcities.txt", "r", encoding="utf8").read().lower().strip()
    )
    twowcitieslist = list(twowordcities.split("\n"))

    # turns user input words into list (for city checking)
    listofinput = list(keyword.split(" "))

    stringofinput = " ".join(listofinput).lower()

    # checks if keyword (userinput) has a valid city
    foundcity = False

    # checks for a two or more worded city Ex: New York
    if any(substring in stringofinput for substring in twowcitieslist):
        for substring in twowcitieslist:
            if substring in stringofinput:
                foundcity = True
                citykeyword.append(substring)
                break

        # checks for a one worded city
    elif set(listofinput).intersection(citieslist) and foundcity == False:
        citykeyword = set(listofinput).intersection(citieslist)
        citykeyword = list(citykeyword)
        foundcity = True

    elif foundcity == False:
        citykeyword.append("none")
        # problem, cities such as New york, being passed as york

    if len(weatherkeywords) > 0 and len(citykeyword) > 0:
        data = weatherkeywords + citykeyword
        return data


def response(data):
    city = data[-1]

    cityobservation = mgr.weather_at_place(city)
    woutput = cityobservation.weather
    # for weather question
    outputsent = False
    if "none" in data:
        print(
            "\nBOT: I don't understand what you are telling me. Please reask me the question and make sure it is related to my weather capabilities and includes a real world location!"
        )
        main()
    else:
        if (
            "temperature" in data
            and "rain" in data
            and "humidity" in data
            and "wind" in data
            and "clouds" in data
        ):
            print(
                f"\nBOT: The weather in {city.title()} includes {woutput.detailed_status} with a cloud cover of {woutput.clouds}% and windspeeds of {woutput.wind().get('speed')} mph. Humidity is {woutput.humidity}%, and amount of rain in the last three hours is: {woutput.rain.get('3h',0)}mm. Lastly, the current temperature in {city.title()} is {woutput.temperature('fahrenheit').get('temp')}F."
            )
            outputsent = True
        else:
            if "temperature" in data:
                print(
                    f"\nBOT: The temperature in {city.title()} is {woutput.temperature('fahrenheit').get('temp')}F"
                )
                outputsent = True
            if "rain" in data:
                print(
                    f"BOT: There was {woutput.rain.get('3h',0)}mm of rain in {city.title()} in the last three hours "
                )
                outputsent = True
            if "humidity" in data:
                print(f"\nBOT: The humidity in {city.title()} is {woutput.humidity}%")
                outputsent = True
            if "wind" in data:
                print(
                    f"\nBOT: The windspeed in {city.title()} is {woutput.wind().get('speed')} mph"
                )
                outputsent = True
            if "clouds" in data:
                print(f"\nBOT: The cloudcover in {city.title()} is {woutput.clouds}%")
                outputsent = True

    if outputsent == True:
        exitquestion = input(
            "\nBOT: Is there anything else you would like to ask me? (WRITE YES OR NO) "
        ).lower()
        if exitquestion == "yes" or exitquestion == "y":
            main()
        elif exitquestion == "no" or exitquestion == "n":
            print(
                "\nBOT: I hope I have answered all weather related questions you may of had!"
            )
            closingmessage = "Deactivating WeatherBOT..........."
            for letter in closingmessage:
                sys.stdout.write(letter)
                sys.stdout.flush()
                time.sleep(0.03)
            print("\nWeatherBOT Deactivated")
            sys.exit()
        else:
            print(
                "\nBOT: You answer isn't yes or no, please answer correctly this time or the program will close."
            )
            exitquestion = input("")
            if exitquestion == "yes" or exitquestion == "y":
                main()
            else:
                print(
                    "\nBOT: I hope I have answered all weather related questions you may of had!"
                )
                closingmessage = "Deactivating WeatherBOT..........."
                for letter in closingmessage:
                    sys.stdout.write(letter)
                    sys.stdout.flush()
                    time.sleep(0.03)
                print("\nWeatherBOT Deactivated")
                sys.exit()


if __name__ == "__main__":
    Wmsg = "\nBOT: Welcome to weatherBOT! I will give you current weather details on any city in the world.\nYou can also ask me specific questions about Temperature, Cloud Cover, Rainfall, Humidity, and Wind Speed! "
    print(Wmsg)
    main()


# this stuff was just mrs greco crap

# phrases to reconize (Enrique)
# hi
# hello
# yo
# nice to meet you
# what
# hey
# sup
# wsg
# forcast
# weather forcast
# weather
# cloud cover
# full
# rain percentage
# orlando
# kississmee
# tampa
# miami
# atlanta
# seattle
# new york
# california
# san diego
# san francisco
# las vegas
# boston
# manhattan
# washington dc
# dallas
# new orleans
# detroit
# chicago
# denver
# philadelphia
# nashville
# clearwater
# ft. luaderdale
# st. augustine
# honolulu
# los angeles
# houston
# phoenix
# san antonio
# san jose
# austin
# columbus
# indianapolis
# charlotte
# portland
# memphis
# louisville
# baltimore
# milwaukee
# albuquerque
# sacremento
# kansas city
# long beach
# oakland
# tulsa
# cleveland
# cincinnati
# newark
# aubrey
# pittsburgh
# st louis
# jersey city
# buffalo
# irving
# st petersburg
# chesapeake
# richmond
# scottsdale
# storm
# detailed status
# heat index
# humidity
# flood
# tornado
# volcano
# wind
# wind speed
# is the
# in
# percentage
# snow
# blizzard
# rainstorm
# severe
# lightning
# thunder
# thunderstorm
# lightningstorm
# conway
# budapest
# barcelona
# madrid
# moscow
# narobi
# paris
# temperature
# Berlin (Last phrase to reconise)


# phrases to say back (ALFONSO)
# hello user what weather information do you need?
# hi user what weather information do you need?
# the cloud cover in orlando is 5 percent
# the chance of rain in orlando is 9 percent
# the temperature in orlando is 5C
# What weather information can I help you with today
# There is a lightning storm in Budapest today
# what weather information do you need of orlando?
# what weather information do you need of kississmee?
# what weather information do you need of tampa?
# what weather information do you need of miami?
# what weather information do you need of atlanta?
# what weather information do you need of seattle?
# what weather information do you need of new york city?
# what weather information do you need of california?
# what weather information do you need of san diego?
# what weather information do you need of san francisco?
# what weather information do you need of las vegas?
# what weather information do you need of boston?
# what weather information do you need of manhattan
# what weather information do you need of washington D.C.?
# what weather information do you need of dallas
# what weather information do you need of new orleans?
# what weather information do you need of detroit?
# what weather information do you need of chicago?
# what weather information do you need of denver?
# what weather information do you need of philadelphia?
# what weather information do you need of nashville?
# what weather information do you need of clearwater?
# what weather information do you need of ft. lauderdale?
# what weather information do you need of st. augustine?
# what weather information do you need of honolulu?
# what weather information do you need of los angeles?
# what weather information do you need of houston?
# what weather information do you need of phoenix?
# what weather information do you need of san antonio?
# what weather information do you need of denver
# the temperature in miami is 15C
# the temperature in berlin is 6C
# the temperature in Moscow is 0C
# the temperature in Alanta is 3C
# the temperature in Madrid is 8C
# the temperature in Barcelona is 10C
# the temperature in Malaga is 20C
# the temparature in Paris is 10C
# the temparature in London is 10C
# the temparture  in Budapest is 10 C
# the temperature in Kyiv is 8C
# the temperature in Los Angoles is 6C
# the temperature in Hamburh is 5C
# the temperature in New York is 10C
# the temparature in Bejing is 2C
# the temparature in Hong Kong is 5C
# the temparture  in Seoul is 2C
# the cloud cover in Los angeles is 5%
# the cloud cover in Manhattan is 20%
# the cloud cover in Madrid is 15%
# the cloud cover in Barcelona is 17%
# the cloud cover in Berlin is 39%
# the cloud cover in Frankfurt is 48%
# the cloud cover in Munich is 34%
# the cloud cover in Manchester is 52%
# the cloud cover in London is 49%
# the cloud cover in Liverpool is 37%
# the cloud cover in Girona is 22%
# the cloud cover in Orlando is 11%
# the cloud cover in Kansas City is 65%
# the cloud cover in Boston is 70%
# the cloud cover in Paris is 12%
# the detailed report in Berlin is overcast with temperatures of 6c and cloud cover of 8%
# the detailed report in Moscow is thunderstorm with temperatures of 2c and cloud cover of 50%
# the detailed report in London is Clear skies with temperatures of 15c and cloud cover of 1%
# the detailed report in Orlando is Slightly cloudy with temperatures of 8c and cloud cover of 20%
# the humidity in Manchester is 10%
# the humidity in Orlando is 14%
# the humidity in Miami is 82%
# the humidity in Gainsville is 65%
# the humidity in Munich is 15%
# the humidity in Hamburg is 5%
# the wind speed in Bangkok is 24 mph
# the wind speed in Hanoi is 64 mph
# the wind speed in Manila is 10 mph
# the wind speed in San Francisco is 11
# the wind speed in Seattle is 9 mph
# the wind speed in Bejing is 4 mph
# the wind speed in Orlando is 6 mph
# the wind speed in Berlin is 5 mph
# the wind speed in London is 18 mph
# the rain chances are 5% in Conway
# the rain chances are 8% in Little Rock
# the rain chances are 30% in Hoqiuam
# the rain chances are 80% in Aberdeen
# the rain chances are 23% in St Petersburg
# the rain chances are 75% in Moscow
# the rain chances are 68% in Narobi
# the rain chances are 52% in tokyo
# the humidity in St petersburg is 15%
