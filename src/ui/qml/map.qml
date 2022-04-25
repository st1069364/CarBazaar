import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtPositioning 5.15
import QtLocation 5.15

Rectangle {
    width: 401
    height: 531
    visible: true
        Map {
            anchors.fill: parent
            id: osm_map
            center: QtPositioning.coordinate(38.2425, 21.7328)
            copyrightsVisible: true
            zoomLevel:15

            plugin: Plugin{
                name:  "osm"
            }
        }

}



