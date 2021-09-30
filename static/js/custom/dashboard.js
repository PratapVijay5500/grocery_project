$(function () {
    //Json data by api call for order table
    $.get(orderListApiUrl, function (response) {
        if(response) {
            var table = '';
            var totalCost = 0;
            $.each(response, function(index, order) {
                totalCost += parseFloat(order.total);
                table += '<tr data-id="'+ order.order_id +'" data-name="'+ order.customer_name +'" data-price="'+ order.total +'">' +
                    '<td>'+ order.order_id +'</td>'+
                    '<td >'+ order.customer_name+'</td>'+
                    '<td>'+ order.total.toFixed(2) +' Rs</td>'+
                    '<td>'+ order.datetime +'</td>'+
                    '<td><button class="btn btn-xs btn-danger delete-customer mr-3">Delete</button></td></tr>';
            });
            table += '<tr><td colspan="2" style="text-align: end"><b>Total</b></td><td><b>'+ totalCost.toFixed(2) +' Rs</b></td></tr>';
            $("table").find('tbody').empty().html(table);
        }
    });
});
 $(document).on("click", ".delete-customer", function (){
        var tr = $(this).closest('tr').remove();
        var data = {
            order_id : tr.data('id')
        };
        var isDelete = confirm("Are you sure to delete Record of "+ tr.data('name') +" ?");
        if (isDelete) {
            callApi("POST", customerDeleteApiUrl, data);
        }
    });
function openLoginForm(){
  document.body.classList.add("showLoginForm");
}
function closeLoginForm(){
  document.body.classList.remove("showLoginForm");
}

