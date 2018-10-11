/**
 * Created by aleksandrkarpenko on 24.08.17.
 */

/**
 * training apparatus
 */

$(document).ready(function () {
    resizeDiv();
});

window.onresize = function (event) {
    resizeDiv();
};


var challenge_url;
var challenge_sequence;
var session_id = '';
var current_challenge_id = '';
var board_text = $("#board_text");
var start_btn = $("#start_btn");
var isSequenceDisplayed = false;

$("#menu-item-challenges").addClass("active");

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

function start_session() {
    var date_now = new Date($.now());
    if (session_id == '') {
        $.ajax({
            url: '/statistic/start_statistic',
            type: 'POST',
            data: {session_start_at: date_now.toISOString(), session_end_at: date_now.toISOString()},
            success: function (json) {
                session_id = json.session_id;
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        })
    }
}

function update_session_end_time() {
    var date_now = new Date($.now());
    if (session_id != '') {
        $.ajax({
            url: '/statistic/update_statistic_time',
            type: 'POST',
            data: {session_id: session_id, session_end_at: date_now.toISOString()},
            success: function (json) {
                console.log(json);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        })
    }
}

function add_answer_to_session(is_right_answer) {
    if (session_id != '' && current_challenge_id != '') {
        isSequenceDisplayed = false;
        $.ajax({
            url: '/statistic/add_answer',
            type: 'POST',
            data: {session_id: session_id, challenge_id: current_challenge_id, is_right: is_right_answer},
            success: function (json) {
                console.log(json);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        })
    }
}

function setBoardMessage(message) {
    board_text.css("font-size", '5em');
    board_text.text("");
    board_text.text(message);
}

$(function () {
    $(".li-level").click(function () {
        if ($(this).attr("value") != 0) {
            challenge_url = $(this).attr("value");
            addStartButton();
            clearAdditionalViews();
            setBoardMessage("Можем начинать!")
        }
    })
});

$(function () {
    $(".menu-list li").click(function () {
        $(".menu-list li").removeClass("active");
        $(this).addClass("active");
    });
});

start_btn.click(function () {
    $.get(challenge_url, function (data) {
        if (challenge_url != null) {
            challenge_sequence = data.sequence;
            current_challenge_id = data.challenge_id;
            //start_session();
            countdown();
            update_session_end_time();
            $("#start_btn").attr("disabled", true);
            clearAdditionalViews();
        } else {
            setBoardMessage("Для начала нужно выбрать тему, уровень и сложность, затем мы сможем начать")
        }
    });
});

var expressionsOperators = [];
var expressionsDigits = [];
var full_expression = "";

function showSequence(sequence) {
    expressionsOperators = [];
    expressionsDigits = [];
    isSequenceDisplayed = false;
    full_expression = "";
    sequence = sequence.split(";");
    var expressions = [];
    var regDigits = /(?:\d*\.)?\d+/g;
    var regOperators = /[-*+\[\]\/]/g;
    for (var i = 0; i < sequence.length; i++) {
        expressionsOperators[i] = sequence[i].match(regOperators);
        expressionsDigits[i] = sequence[i].match(regDigits);
        expressions[i] = sequence[i].match(regOperators) + " " + sequence[i].match(regDigits);
        // if (i == 0) {
        //     full_expression += sequence[i].match(regDigits) + " ";
        // } else {
        //     full_expression += expressions[i] + " ";
        // }
    }

    board_text.css("font-size", '10em');
    var i = 0;
    var timerId = setInterval(function () {
        board_text.text(expressions[i]);
        i++;
    }, 800);
    setTimeout(function () {
        clearInterval(timerId);
        i = 0;
        setBoardMessage('Какой ответ?');
        isSequenceDisplayed = true;
        // start_btn.attr("disabled", false);
        $("#start_btn").attr("disabled", false);
        // start_btn.attr("data-role", "replay");
        $("#start_btn").attr("data-role", "replay");
        addAnswerInput();
    }, ((expressions.length + 1) * 800));
}

function answerIs(expressionsDigits, expressionsOperators) {
    var result = 0;
    full_expression = "";
    for (var i = 0; i < expressionsDigits.length; i++) {
        var digit = parseInt(expressionsDigits[i]);
        switch (expressionsOperators[i] + "") {
            case '+':
                result += digit;
                break;
            case '-':
                result -= digit;
                break;
            case '*':
                result = result * digit;
                break;
            case '/':
                result = result / digit;
                break;
            default:
                result = "Ошибка";
        }
        full_expression += expressionsOperators[i] + digit;
    }
    return result;
}

function countdown() {
    var message = ["Готов?", "Начали!"];
    var i = 0;
    var timerId = setInterval(function () {
        setBoardMessage(message[i]);
        i++;
    }, 1000);
    setTimeout(function () {
        clearInterval(timerId);
        i = 0;
        showSequence(challenge_sequence);
    }, ((message.length + 1) * 1000));
}

var delayTimer;

function checkAnswer(answer) {
    clearTimeout(delayTimer);
    delayTimer = setTimeout(function () {
        answr = parseInt(answer);
        if (isNumber(answr)) {
            update_session_end_time();
            $("#right-answer-btn").remove();
            var a = answerIs(expressionsDigits, expressionsOperators);
            if (a != "Ошибка") {
                if (answr == a) {
                    setBoardMessage("Молодец! Ответ верный!");
                    clearAdditionalViews();
                    add_answer_to_session('True');
                    $("#start_btn").focus();
                } else {
                    setBoardMessage("К сожалению, ответ неверный!");
                    addCheatButton(a)
                }
            } else {
                setBoardMessage("Произошла ошибка, обратись к администратору");
            }
        }
    }, 1000);
    // else {
    //     setBoardMessage("Произошла ошибка, обратись к администратору");
    // }
}

function clearAdditionalViews() {
    $("#answer-input").remove();
    $("#right-answer-btn").remove();
}

function addCheatButton(answer) {
    $("#right-answer-btn").remove();
    $(".board-content").append('<div><button id="right-answer-btn" class="btn btn-answer" type="button">Узнать ответ</button></div>');
    $("#right-answer-btn").click(function () {
        update_session_end_time();
        clearAdditionalViews();
        setBoardMessage(full_expression + " = " + answer);
        add_answer_to_session('False');
        $("#start_btn").focus();
    });
}

function addStartButton() {
    $("#start_btn").remove();
    $("#under-board").append('<button class="btn-start" id="start_btn" data-role="play"></button>');
    $("#start_btn").focus();
    $("#start_btn").click(function () {
        $.get(challenge_url, function (data) {
            if (challenge_url != null) {
                challenge_sequence = data.sequence;
                current_challenge_id = data.challenge_id;
                start_session();
                update_session_end_time();
                if (isSequenceDisplayed) {
                    add_answer_to_session("False");
                }

                clearAdditionalViews();
                setBoardMessage("");
                countdown();
                $("#start_btn").attr("disabled", true);
            } else {
                setBoardMessage("Для начала нужно выбрать тему, уровень и сложность, затем мы сможем начать")
            }
        });
    });
}

function addAnswerInput() {
    $("#answer-input").remove();
    $(".board-content").append('<input id="answer-input" class="answer-input " type="number" placeholder="Введи ответ">');
    $("#answer-input").focus();

    // var answerInputDelay;
    // $(document).on('input', '#answer-input', function () {
    //     clearTimeout(answerInputDelay);
    //     answerInputDelay = setTimeout(function () {
    //         checkAnswer($("#answer-input").val());
    //         //ToDo вот тут хуйня
    //     }, 1000);
    // });
    $(document).on('input', '#answer-input', function () {
        checkAnswer($("#answer-input").val());
    });
}

function resizeDiv() {
    vpw = $(window).width();
    vph = $(window).height() - 250;
    $(".board").css({'min-height': vph + 'px'});
}

function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}