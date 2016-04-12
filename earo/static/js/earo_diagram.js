/*
Copyright 2016 Everley

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
const Color = {
    'Red'   : 1,
    'Blue'  : 2,
    'Green' : 3,
    'Yellow': 4,
    'Grey'  : 5,
} 

const ContentType = {
    'Text'  : 1,
    'Table' : 2,
}

function color_to_class(color) {
    color_class = null;
    switch(color) {
    case Color.Red:
        color_class = "panel-danger";
        break;
    case Color.Blue:
        color_class = "panel-primary";
        break;
    case Color.Green:
        color_class = "panel-success";
        break;
    case Color.Yellow:
        color_class = "panel-warning";
        break;
    case Color.Grey:
        color_class = "panel-default";
        break;
    default:
        color_class = "panel-default";
    } 
    return color_class;
}

function fill_content(element, content) {
    switch(content.content_type) {
    case ContentType.Text:
        element.text(content.text);
        break;
    case ContentType.Table:
        var dom_table = $("<table class=\"table\"></table>");
        element.append(dom_table);

        var dom_thead = $("<thead></thead>");
        dom_table.append(dom_thead);
        var dom_tr = $("<tr></tr>"); 
        dom_thead.append(dom_tr);
        for (var i = 0; i < content.table_head.length; ++i) {
            var dom_th = $("<th></th").text(content.table_head[i]);
            dom_tr.append(dom_th);
        }

        var dom_tbody = $("<tbody></tbody>");
        dom_table.append(dom_tbody);
        for (var i = 0; i < content.table_rows.length; ++i) {
            var dom_tr = $("<tr></tr>"); 
            dom_tbody.append(dom_tr);
            for (var j = 0; j < content.table_rows[i].length; ++j) {
                var dom_th = $("<th></th").text(content.table_rows[i][j]);
                dom_tr.append(dom_th);
            }
        }
    }
}

function make_cable(left, top, height) {
    var cable = $("<div class=\"cable\" style=\"left:{0}px;top:{1}px;height:{2}px;\"></div>".format(left - 2, top - 2, height));
    return cable;
}

function make_point(left, top) {
    var point = $("<div class=\"circle\" style=\"left:{0}px;top:{1}px;\"></div>".format(left - 5, top - 5));
    return point;
}

function build_diagram(root_panel) {
    var body_padding_left = 50;
    var col_offset = 180; 
    var row_offset = 40;
    var bottom_of_col = new Array()  

    var build_panel_recursively = function(panel, row, col, last_panel_tail_x = -1, last_panel_tail_y = -1) {
        var x = col_offset * col + body_padding_left; 
        var y = 0;

        for (var i = 0; i < bottom_of_col.length; ++i) {
            y = Math.max(y, bottom_of_col[i]); 
        } 

        y += row_offset;

        var dom_panel = $("<div class=\"panel earo-panel {0}\" style=\"left:{1}px;top:{2}px;\"></div>".format(color_to_class(panel.color), x ,y));
        $("body").append(dom_panel)

        var dom_heading = $("<div class=\"panel-heading\"></div>");
        dom_panel.append(dom_heading)

        if (panel.title) {
            var dom_title = $("<div class=\"panel-title\"></div>"); 
            fill_content(dom_title, panel.title)
            dom_heading.append(dom_title);
        }
        
        if (panel.body) {
            var dom_body = $("<div class=\"panel-body\"></div>"); 
            fill_content(dom_body, panel.body)
            dom_panel.append(dom_body);
        }

        if (panel.footer) {
            var dom_footer = $("<div class=\"panel-footer\"></div>"); 
            fill_content(dom_footer, panel.footer)
            dom_panel.append(dom_footer);
        }

        var title_height = dom_heading.outerHeight(); 
        var panel_height = dom_panel.height();
        var bottom = y + panel_height;
        bottom_of_col[col] = bottom;

        if (last_panel_tail_x > 0 
            && last_panel_tail_y > 0
        ) {
            var cable_left = x;
            var cable_top = last_panel_tail_y;
            var cable_height = y - last_panel_tail_y;
            var cable = make_cable(cable_left, cable_top, cable_height);
            $("body").append(cable);

            var start_point_x = last_panel_tail_x;
            var start_point_y = last_panel_tail_y + 2;
            var start_point = make_point(start_point_x, start_point_y);
            $("body").append(start_point);

            var end_point_x = x;
            var end_point_y = y;
            var end_point = make_point(end_point_x, end_point_y);
            $("body").append(end_point);
        }
         
        var panel_tail_x = x + col_offset 
        var panel_tail_y = bottom
        for (var i = 0; i < panel.next_panels.length; ++i) {
            build_panel_recursively(panel.next_panels[i], row + i + 1, col + 1, panel_tail_x, panel_tail_y);
        }
    }
    build_panel_recursively(root_panel, 0, 0)
}
