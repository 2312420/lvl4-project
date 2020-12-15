

const price_div = $('#price_div')

let company_ajax_call = function (endpoint) {
	$.getJSON(endpoint)
		.done(response => {
            console.log(response['html_from_view'])
			price_div.fadeTo('fast', 0).promise().then(() => {

				price_div.html(response['html_from_view'])

				price_div.fadeTo('fast', 1)

			})
		})
}

setInterval(function () {
    let endpoint = document.location.pathname
    company_ajax_call(endpoint)
}, 5000);