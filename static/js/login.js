/**
 * Created by Nightsuki on 2015/11/21.
 */
$(document).ready(function () {
    $("#login").click(function () {
        $.ajax({
            url: '/ajax/login',
            type: "POST",
            data: {
                username: $('#username').val(),
                password: $('#password').val()
            },
            success: function (r) {
                if (r.status === '1') {
                    window.location.href = "/list";
                }
                else if (r.status === '0') {
                    alert(r.info);
                }
            },
            error: function (r) {
                alert(r.info);
            }
        });
    });
});