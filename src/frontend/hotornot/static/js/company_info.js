const stock_info_div = $('#stockInfo')

let company_info_ajax_call = function (endpoint) {
	$.getJSON(endpoint, {"t":"info"})
		.done(response => {
			stock_info_div.fadeTo('fast', 0).promise().then(() => {

				stock_info_div.html(response['html_from_view'])

				stock_info_div.fadeTo('fast', 1)

			})
		})
}

let endpoint = document.location.pathname
company_info_ajax_call(endpoint)

