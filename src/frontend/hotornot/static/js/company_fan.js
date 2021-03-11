const stock_fan_div = $('#fan-replace')

let company_fan_ajax_call = function (endpoint) {
	$.getJSON(endpoint, {"t":"fan"})
		.done(response => {
			stock_fan_div.fadeTo('fast', 0).promise().then(() => {

				stock_fan_div.html(response['html_from_view'])

				stock_fan_div.fadeTo('fast', 1)

			})
		})
}

let fan_endpoint = document.location.pathname
company_fan_ajax_call(info_endpoint)