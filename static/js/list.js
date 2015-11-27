/**
 * Created by Nightsuki on 2015/11/21.
 */
$(document).ready(function () {
    $('.back-mask, .close').click(function (e) {
        e.preventDefault();
        $('.back-mask').fadeOut(100);
        $('.http-packet').slideUp(200);
    });
    $("#logout").click(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/ajax/logout',
            type: "POST",
            success: function (r) {
                window.location.href = "/";
            },
            error: function (r) {
                alert(r.info);
            }
        });
    });
    $("#delalldomain").click(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/ajax/delalldomain',
            type: "POST",
            success: function (r) {
                alert("删除成功");
                location.reload();
            },
            error: function (r) {
                alert(r.info);
            }
        });
    });
    $(".deldoamin").click(function (e) {
        e.preventDefault();
        var domain_id = $(this).parents('.domain').attr("id");
        var that = $(this);
        $.ajax({
            url: '/ajax/deldomain',
            type: "POST",
            data: {
                domain_id: domain_id
            },
            success: function (r) {
                if (r.status == 1) {
                    that.parents('.domain').fadeOut();
                    alert("删除成功");
                } else {
                    alert(r.info);
                }
            },
            error: function (r) {
                alert(r.info);
            }
        });
    });

    $(".show").click(function (e) {
        e.preventDefault();
        var domain_id = $(this).parents('.domain').attr("id");
        var that = $(this);
        $(".textarea").each(function () {
            if ($(this).parents('.domain').attr("id") != domain_id) {
                $(this).slideUp();
            } else {
                if ($(this).parents('.domain').find(".textarea").is(':hidden')) {
                    $.ajax({
                            url: '/ajax/domaininfo',
                            type: "POST",
                            data: {
                                domain_id: domain_id
                            },
                            success: function (result) {
                                var dns_text = "<tbody class='dns-body'>";
                                var url_text = "<tbody class='access-body'>";
                                var dns_list = result.info.dns_list;
                                var url_list = result.info.url_list;
                                var temp = "";
                                $.each(dns_list, function (n, dns) {
                                    temp = "<tr><td>" + dns.ip + "</td><td>" + dns.created_time + "<td></tr>\r\n";
                                    dns_text += temp
                                });
                                $.each(url_list, function (n, url) {
                                    temp = "<tr class='" + url.id + "'><td>" + url.url + "</td><td>" + url.ip + "</td><td>" + url.created_time + "</td><td><button type='button' class='httppacket btn btn-info'>Packet</button></td></tr>\r\n";
                                    url_text += temp
                                });
                                dns_text += "</tbody>";
                                url_text += "</tbody>";
                                that.parents('.domain').find(".dns").find(".dns-body").replaceWith(dns_text);
                                that.parents('.domain').find(".access").find(".access-body").replaceWith(url_text);
                                that.parents('.domain').find(".textarea").slideToggle();
                                $(".httppacket").click(function () {
                                    e.preventDefault();
                                    var url_id = $(this).parents('tr').attr("class");
                                    $.ajax({
                                        url: '/ajax/httppacket',
                                        type: "POST",
                                        data: {
                                            url_id: url_id
                                        },
                                        success: function (r) {
                                            $('.http-packet').find("textarea").text(r.info);
                                            $('.back-mask').fadeIn(100);
                                            $('.http-packet').slideDown(200);
                                        },
                                        error: function (r) {
                                            alert(r.info);
                                        }
                                    });
                                });
                            },
                            error: function (result) {
                                alert(result.info);
                            }
                        });
                } else {
                    that.parents('.domain').find(".textarea").slideToggle();
                }
            }
        });

    });
});