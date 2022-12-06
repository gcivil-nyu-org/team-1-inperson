from decouple import config
from landing_map.models import Accessible_location, Infra_type
from report.models import Report
import requests


class reportObject:
    def __init__(self, infraID, createdAt, updatedAt, desc, username):
        self.infraID = infraID
        temp = Accessible_location.objects.filter(infraID=infraID)[0]
        self.username = username
        self.createdAt = createdAt
        self.address = temp.address
        self.infraType = str(temp.typeID)
        self.updatedAt = updatedAt
        self.desc = desc
        self.locationX = temp.locationX
        self.locationY = temp.locationY

    def __str__(self):
        return f"Infra ID: {self.infraID}, Description: {self.desc}"


def get_locations():
    return Accessible_location.objects.all()


def get_recent_reports(num):

    recent_report_list = []
    # report_query = Report.objects.order_by("-createdAt")[:num]
    infra_set = set()
    report_query = Report.objects.order_by("-createdAt")[:num]

    for q in report_query:
        # temp = Accessible_location.objects.filter(infraID=q.infraID.infraID)[0]
        report_q = Report.objects.filter(infraID=q.infraID.infraID)
        # print(report_q)
        comment_list = []
        # user_list = []

        for qObject in report_q:
            comment_list.append(
                (qObject.comment, qObject.user.username, qObject.updatedAt)
            )
            # user_list.append(qObject.user.username)
        # print(type(q.infraID))
        # print(temp)
        # print(comment_list)
        # print(user_list)
        # address = temp.address
        # infraType = str(temp.typeID)
        # print(q.user.username)
        r = reportObject(
            infraID=q.infraID.infraID,
            createdAt=q.createdAt,
            updatedAt=q.updatedAt,
            desc=comment_list,
            username=q.user.username,
        )
        if r.infraID not in infra_set:
            # print("INSIDE IF")
            recent_report_list.append(r)
            # print(len(recent_report_list))
            infra_set.add(r.infraID)
        # print(r.desc)
        # print(infra_set)
    # for rr in recent_report_list:
    #     print(rr)
    # print(len(recent_report_list))

    return recent_report_list


def populate_cards(locList):
    # mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    # loc_list = [(40.68852572417966, -73.98657073016483), (40.68893870107474, -73.9863174112231)]
    # for loc in loc_list:
    # qset = Accessible_location.objects.filter()[:30]
    # print(qset)
    # q1 = Accessible_location(locationX = loc_list[0][1], \
    # locationY = loc_list[0][0], infraID = 1, isAccessible = True, \
    # typeID = Infra_type.objects.get(typeName = "Ramp"))
    # q2 = Accessible_location(locationX = loc_list[1][1], \
    # locationY = loc_list[1][0], infraID = 2, isAccessible = True, \
    # typeID = Infra_type.objects.get(typeName = "Ramp"))
    # qset = [q1,q2]
    # print(qset[0])
    # print(qset[1])
    # res = {}
    final = []
    for q in locList:
        card_info = {}
        comment_list = []
        # print(q)
        # params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}
        # url = mapbox_host + str(q.locationX) + "," + str(q.locationY) + ".json"
        # response = requests.get(url=url, params=params).json()
        # address = response["features"][0]["place_name"]

        location = Accessible_location.objects.filter(infraID=q.infraID)[0]
        address = location.address
        x = location.locationX
        y = location.locationY
        # print(len(address))
        # address = ' '.join(address.split(" ")[1:])

        # if card_info.get(address) is None:
        #     card_info[address] = {}

        # get report for each q
        report_q = Report.objects.filter(infraID=q.infraID).order_by("-updatedAt")
        for qObject in report_q:
            comment_list.append(
                (qObject.comment, qObject.user.username, qObject.updatedAt)
            )
        # print(report)
        # print(len(report))
        if len(report_q) != 0:
            # print(report)
            report = report_q[0]
            comment = comment_list
            created = report.createdAt
            updated = report.updatedAt
        else:
            comment = ""
            created = ""
            updated = ""

        card_info["text"] = address
        card_info["type"] = str(q.typeID)
        card_info["card_id"] = q.infraID
        card_info["comment"] = comment
        card_info["time_reported"] = created
        card_info["last_update"] = updated
        card_info["x"] = x
        card_info["y"] = y
        # if str(q.typeID) == "Ramp":
        if q.isAccessible:
            card_info["isAccessible"] = True
        else:
            card_info["isAccessible"] = False
        # print(card_info)
        # print(cardList)
        final.append(card_info)
    # address_list = []
    # for card in cardList:
    #     address_list.append(card)
    # address_list = card.keys()
    return final


def populate_cards_by_address():
    cardList = []
    # mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    # loc_list = [(40.68852572417966, -73.98657073016483), (40.68893870107474, -73.9863174112231)]
    # for loc in loc_list:
    qset = Accessible_location.objects.filter()[:30]
    # print(qset)
    # q1 = Accessible_location(locationX = loc_list[0][1], \
    # locationY = loc_list[0][0], infraID = 1, isAccessible = True, \
    # typeID = Infra_type.objects.get(typeName = "Ramp"))
    # q2 = Accessible_location(locationX = loc_list[1][1], \
    # locationY = loc_list[1][0], infraID = 2, isAccessible = True, \
    # typeID = Infra_type.objects.get(typeName = "Ramp"))
    # qset = [q1,q2]
    # print(qset[0])
    # print(qset[1])
    card_id = 1
    card_info = {}
    # res = {}
    final = []
    address_set = set()

    for q in qset:
        # print(q)
        # params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}
        # url = mapbox_host + str(q.locationX) + "," + str(q.locationY) + ".json"
        # response = requests.get(url=url, params=params).json()
        address = Accessible_location.objects.filter(infraID=q.infraID)[0].address
        address = " ".join(address.split(" ")[1:])
        if card_info.get(address) is None:
            card_info[address] = {}
        if str(q.typeID) == "Ramp":
            if q.isAccessible:
                # print("BEFORE UPDATE: ", card_info[address])
                # print("INSIDE IF: ", card_info[address].get("ramp_count"))
                card_info[address]["ramp_count"] = (
                    card_info[address].get("ramp_count", 0) + 1
                )
            else:
                card_info[address]["isRampAccess"] = False

        elif str(q.typeID) == "Signal":
            if q.isAccessible == "True":
                card_info[address]["signal_count"] = (
                    card_info[address].get("signal_count", 0) + 1
                )
            else:
                card_info[address]["isSignalAccess"] = False

        elif str(q.typeID) == "Raised_Crosswalk" and str(q.isAccessible):
            try:
                card_info[address]["rcross_count"] = (
                    card_info[address].get("rcross_count", 0) + 1
                )
            except KeyError:
                card_info[address]["rcross_count"] = 0

        try:
            if card_info[address]["signal_count"] is not None:
                pass
        except KeyError:
            card_info[address]["signal_count"] = 0

        try:
            if card_info[address]["ramp_count"] is not None:
                pass
        except KeyError:
            card_info[address]["ramp_count"] = 0

        try:
            if card_info[address]["rcross_count"] is not None:
                pass
        except KeyError:
            card_info[address]["rcross_count"] = 0

        try:
            if card_info[address]["isRampAccess"] is not None:
                pass
        except KeyError:
            card_info[address]["isRampAccess"] = True

        try:
            if card_info[address]["isSignalAccess"] is not None:
                pass
        except KeyError:
            card_info[address]["isSignalAccess"] = True

        if card_info[address].get("card_id") is None:
            card_info[address]["card_id"] = card_id
            card_id += 1
        # print(card_info)
        if address not in address_set:
            cardList.append(card_info)
            address_set.add(address)
    # print(cardList)
    # address_list = []
    # for card in cardList:
    #     address_list.append(card)
    # address_list = card.keys()
    for card, address in zip(cardList, address_set):
        res = {}
        print(address)
        res["text"] = address
        res["ramp_count"] = card[address]["ramp_count"]
        res["signal_count"] = card[address]["signal_count"]
        res["rcross_count"] = card[address]["rcross_count"]
        res["card_id"] = card[address]["card_id"]
        res["isRampAccess"] = card[address]["isRampAccess"]
        res["isSignalAccess"] = card[address]["isSignalAccess"]
        # print(res)
        final.append(res)
        print(final)

    return final


def populate_favorite_cards(favList):
    flist = []
    id = 1
    for fav in favList:
        fav_card_info = {}

        x_coord = fav.locationX
        y_coord = fav.locationY
        address = fav.address

        rampsQuery = (
            "SELECT infraID, isAccessible, ( 3959 * acos( cos( radians({y}) ) * cos( radians(locationY) ) * cos( radians(locationX) "
            "- radians({x}) ) + sin( radians({y}) ) * sin(radians(locationY)) ) ) AS distance FROM landing_map_accessible_location "
            "where typeID_id = 1 and isAccessible = 0 HAVING distance < "
            "{radius} ORDER BY distance".format(
                y=y_coord,
                x=x_coord,
                radius=0.25,
            )
        )
        signalsQuery = (
            "SELECT infraID, isAccessible, ( 3959 * acos( cos( radians({y}) ) * cos( radians(locationY) ) * cos( radians(locationX) "
            "- radians({x}) ) + sin( radians({y}) ) * sin(radians(locationY)) ) ) AS distance FROM landing_map_accessible_location "
            "where typeID_id = 2 and isAccessible = 0 HAVING distance < "
            "{radius} ORDER BY distance".format(
                y=y_coord,
                x=x_coord,
                radius=0.25,
            )
        )
        alert = ""
        ramps = Accessible_location.objects.raw(rampsQuery)
        for ramp in ramps:
            if not ramp.isAccessible:
                alert = "Report found near this location!"
                break
        signals = Accessible_location.objects.raw(signalsQuery)
        for signal in signals:
            if not signal.isAccessible:
                alert = "Report found near this location!"
                break

        fav_card_info["address"] = address
        fav_card_info["x"] = x_coord
        fav_card_info["y"] = y_coord
        fav_card_info["count_ramps"] = len(ramps)
        fav_card_info["count_signals"] = len(signals)
        fav_card_info["alert"] = alert
        fav_card_info["id"] = id
        flist.append(fav_card_info)
        id += 1
    return flist


def getAddressFromMapbox(long, lat):
    mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}
    url = mapbox_host + str(long) + "," + str(lat) + ".json"
    response = requests.get(url=url, params=params).json()
    address = response["features"][0]["place_name"]
    return address
