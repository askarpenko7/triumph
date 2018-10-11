//Made 4 show statistics.
$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#menu-item-statistic").addClass("active");
    $("#menu-item-challenges-ref").attr('href', '/');
    var date_start_picker = $("#date_start");
    var date_end_picker = $("#date_end");
    var generate_btn = $("#generate_stat");
    var group_selector = $("#groups-selector");
    var student_selector = $("#students-selector");
    var date_format = "dd-mm-yy";
    var current_url = window.location.href;
    var date_start = "m_ago";
    var date_end = "today";
    var dates = current_url.match(/(\d{2}-\d{2}-\d{4}|m_ago|today)/g);
    var filters_state = current_url.match(/\/([0-9]+|g_all)\/([0-9]+|s_all)/g);
    var groups_state = "g_all";
    var students_state = "s_all";
    if (filters_state != null) {
        groups_state = filters_state[0].match(/(\d|g_all|s_all)/g)[0];
        students_state = filters_state[0].match(/(\d|g_all|s_all)/g)[1];
    }
    if (groups_state != null) {
        group_selector.val(groups_state);
    }
    if (students_state != null) {
        student_selector.val(students_state);
    }

    if (dates) {
        if (dates.length > 0) {
            date_start = dates[0];
            date_end = dates[1];
        }
    }

    $(function () {
        date_start_picker.datepicker({
            showOtherMonths: true,
            selectOtherMonths: true,
            showButtonPanel: true,
            dateFormat: date_format,
            onSelect: function (dateText, inst) {
                date_start = dateText;
            }
        });
        date_start_picker.attr('readonly', true);
        date_start_picker.datepicker("setDate", date_start == "m_ago" ? "-30" : date_start);

        date_end_picker.datepicker({
            showOtherMonths: true,
            selectOtherMonths: true,
            showButtonPanel: true,
            dateFormat: date_format,
            onSelect: function (dateText, inst) {
                date_end = dateText;
            }
        });
        date_end_picker.attr('readonly', true);
        date_end_picker.datepicker("setDate", date_end == "toady" ? "0" : date_end);

    });

    group_selector.change(function () {
        getSelectorsData(group_selector.val());
    });


    $(function () {
        generate_btn.click(function () {
            var group = group_selector.val() != null ? group_selector.val() : "g_all";
            var student = student_selector.val() != null ? student_selector.val() : "s_all";
            var date_s = date_start != null ? date_start : "m_ago";
            var date_e = date_end != null ? date_end : "today";
            window.location.replace('/statistic/' + group + '/' + student + '/' + date_s + '/' + date_e + '/');
        })
    });

    resizeDiv();

    function getSelectorsData(group_id) {
        $.ajax({
            url: '/statistic/get_users_by_group/' + group_id,
            type: 'GET',
            success: function (json) {
                var users = json.users;
                student_selector.empty();
                student_selector.append($("<option></option>")
                    .attr("value", "s_all")
                    .text("Все ученики"));
                users.forEach(function (user, i, users) {
                    student_selector.append($("<option></option>")
                        .attr("value", user.user_id)
                        .text(user.user_name));
                })
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        })
    }
});

window.onesize = function (event) {
    resizeDiv();
};

function resizeDiv() {
    vpw = $(window).width();
    vph = $(window).height() - $(".stat-filters-container").height() - 60;
    $(".stat-board").css({'min-height': vph + 'px'});
}


