$(main);


function main() {
    $("a.img_link").click(load_image);
    $("body").addClass("loaded");
    $("td.text p").map(mfm_to_highlights);
    $("td.lnum").map(add_line_numbers);
};


function add_line_numbers() {
    //find text
    var text = $(this).siblings("td:last").text();
    var line_count = text.split("\n").length;
    var count = 1;
    var line_num_string = "";
    while(count < line_count) {
        line_num_string += count + "\n";
        count++;
    }
    $(this).append($("<p>" + line_num_string + "</p>"));
}

function load_image(ev) {
    $(this).parent().removeClass("img_ph");
    var src = $(this).attr("href");
    var img = $("<div class='img_cont'><a href='" + src +"\'><img src='" + src + "'/></a></div>");
    $(this).replaceWith(img);
    return false;
};

function mfm_to_highlights() {
    var text = $(this).text();
    if(text.search(/{{|}}/) == -1) {return;}
    text = text.replace(/{{/g, "<span class='highlight'>");
    text = text.replace(/}}/g, "</span>");
    $(this).replaceWith($("<p>" + text + "</p>"));
};