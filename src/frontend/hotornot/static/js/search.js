const user_input = $("#user-input")
const search_icon = $('#search-icon')
const company_div = $('#replaceable-content')
const endpoint = '/hotornot/'
const delay_by_in_ms = 300
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {

			company_div.fadeTo('fast', 0).promise().then(() => {

				company_div.html(response['html_from_view'])

				company_div.fadeTo('fast', 1)

				search_icon.removeClass('blink')
			})
		})
}


user_input.on('keyup', function () {
	const request_parameters = {
		q: $(this).val()
	}

	search_icon.addClass('blink')

	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})