from link.base.link import Link


class UserEquipmentToBaseStationLink(Link):
    def __init__(self, source_node, destination_node, channel):
        super().__init__(source_node, destination_node, channel)
