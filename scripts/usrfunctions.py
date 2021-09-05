

from folium import Marker

# color code function
def colorcode(x):
    if x in range(0,1600):
        color = 'blue'
        icon = 'heartbeat'
    elif x in range(1601,6000):
        color = 'orange'
        icon = 'exclamation-circle'
    else:
        color = 'red'
        icon = 'fa-ambulance'
    return (color, icon)

# function for diff. markers
# THANKS TO: https://stackoverflow.com/questions/56842575/how-to-display-averages-instead-of-counts-on-folium-markerclusters
class MarkerWithProps(Marker):
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        var {{this.get_name()}} = L.marker(
            [{{this.location[0]}}, {{this.location[1]}}],
            {
                icon: new L.Icon.Default(),
                {%- if this.draggable %}
                draggable: true,
                autoPan: true,
                {%- endif %}
                {%- if this.props %}
                props : {{ this.props }} 
                {%- endif %}
                }
            )
            .addTo({{this._parent.get_name()}});
        {% endmacro %}
        """)
    def __init__(self, location, popup=None, tooltip=None, icon=None,
                 draggable=False, props = None ):
        super(MarkerWithProps, self).__init__(location=location,popup=popup,tooltip=tooltip,icon=icon,draggable=draggable)
        self.props = json.loads(json.dumps(props))    


# icon creation function
def icon_create_function():

    jsScriptString = """
    function(cluster) {

    var c = ' marker-cluster-';

    var markers = cluster.getAllChildMarkers();
    var sum = 0;
    for (var i = 0; i < markers.length; i++) {
        sum += markers[i].options.props.population;
    }
    var sum_total = sum;

    if (sum_total < 1600) {
        c += 'small';
    } else if (sum_total < 6000) {
        c += 'medium';
    } else {
        c += 'large';
    }

    return new L.DivIcon({ html: '<div><span style="font-size: 7pt">' + sum_total + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
    }
    """
    return jsScriptString


# THANKS TO: https://stackoverflow.com/questions/37466683/create-a-legend-on-a-folium-map
def legend_html():
    item_txt = """<br> &nbsp; <i class="fa fa-map-marker fa-2x" style="color:{col}"></i> &nbsp; {item}"""
    item_clu = """<br> &nbsp; <i class="fa fa-circle-o fa-lg" aria-hidden="true" style="color:{col}"></i> &nbsp; {item}"""
    html_itms_1 = item_txt.format(item="Menos de 1600", col="#82CAFA")
    html_itms_2 = item_txt.format(item="Entre 1600 y 6000", col="orange")
    html_itms_3 = item_txt.format(item="Más de 6000", col="red")
    html_itms_4 = item_clu.format(item="Contagios en el área", col="green")

    htmlString = (
        '''
        <div style="
        position: fixed; 
        top: 120px; left: 20px; width: 150px; height: 100px; margin:0 auto;
        border:2px solid grey; z-index:9999; 
        background-color:white;
        opacity: .55;
        font-size:10px;
        font-weight: bold;
        line-height: 12px
        "> 
        &nbsp; 
        {itm_txt_4}
        {itm_txt_1}
        {itm_txt_2}
        {itm_txt_3}
        </div>
        '''.format(itm_txt_1=html_itms_1, itm_txt_2=html_itms_2, itm_txt_3=html_itms_3, itm_txt_4=html_itms_4)
    )

    return htmlString

def title_html():

    htmlString = (
        '''
        <div style="
        position: fixed; 
        top: 80px; left: 10px; width: 260px; 
        height: 35px; line-height: 35px; text-align: center;
        border:2px solid grey; z-index:9999; 
        border-radius: 25px;
        background-color:white;
        opacity: .55;
        font-size:12px;
        font-family: fantasy; 
        "> 
        {title}
        </div>
        '''.format(title="COVID-19 en Perú, contagios por distrito")
    )
    
    return htmlString
