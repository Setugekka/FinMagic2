/*
初始化trend_prediction_sorting_base模板
Author: fzjie
File: jquery.trend_prediction_sorting_base
*/
$(document).ready(function () {
// activate the trend_prediction_sorting_base menu in based on url
    $("#trend_prediction_sorting_navigation a").each(function () {
        var pageUrl = window.location.href.split(/[?#]/)[0];
        var this_url=this.href.split(/[?#]/)[0];
        if ( this_url== pageUrl) {
            $(this).removeClass("btn-secondary")
            $(this).addClass("btn-primary");
        }
    });
});
