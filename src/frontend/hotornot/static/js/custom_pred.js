const loader = document.getElementById("graphLoader");

const pred_div = $('#customGraph')

let pred_ajax_call = function (endpoint,) {
	$.getJSON(endpoint, {"t":"pred"})
		.done(response => {
			pred_div.fadeTo('fast', 0).promise().then(() => {
                loader.hidden = true;

				pred_div.html(response['html_from_view'])

				pred_div.fadeTo('fast', 1)

			})
		})
}



$('#post-form').on('submit', function(event){
    event.preventDefault();
    var form = $(this);

    pred_div.fadeTo('fast',0).promise().then(() => {
        var op = 0;  // initial opacity
        loader.style.opacity = 0;
        loader.hidden = false;
        var timer = setInterval(function () {
            if (op > 1) {
                clearInterval(timer);
                $.getJSON(document.location.pathname, form.serialize())
		        .done(response => {
			        pred_div.fadeTo('fast', 0).promise().then(() => {
                    loader.hidden = true;
				    pred_div.html(response['html_from_view'])
				    pred_div.fadeTo('fast', 1)
			})
		})

            }
            op += 0.1
            loader.style.opacity = op;
        }, 50);
    })
    //red_ajax_call(document.location.pathname)
    //console.log("form submitted!")

});