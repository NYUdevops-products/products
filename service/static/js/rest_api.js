$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_category").val(res.category);
        $("#product_amount").val(res.amount);
        $("#product_likecount").val(res.likecount);
        $("#product_status").val(res.status);
        // if (res.available == true)
        //     $("#product_available").val("true");
        // } else {
        //     $("#product_available").val("false");
        // }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_category").val("");
        $("#product_amount").val("");
        $("#product_likecount").val("");
        $("#product_status").val("");
        // $("#product_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a product
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#product_name").val();
        var category = $("#product_category").val();
        var amount = $("#product_amount").val();
        var likecount = $("#product_likecount").val();
        var status = $("#product_status").val();
        // var available = $("#product_available").val() == "true";
        

        var data = {
            "name": name,
            "category": category,
            "amount": amount,
            "likecount": likecount,
            "status": status
            // "available": available
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a product
    // ****************************************

    $("#update-btn").click(function () {

        var product_id = $("#product_id").val();
        var name = $("#product_name").val();
        var category = $("#product_category").val();
        var amount = $("#product_amount").val();
        var likecount = $("#product_likecount").val();
        var status = $("#product_status").val();
        // var available = $("#product_available").val() == "true";

        var data = {
            "name": name,
            "category": category,
            "amount": amount,
            "likecount": likecount,
            "status": status
            // "available": available
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/products/" + product_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a product
    // ****************************************

    $("#retrieve-btn").click(function () {

        var product_id = $("#product_id").val();
        var product_name=$("#product_name").val();
        var queryString = ""
        if (product_id){
            queryString = product_id
        }

        if (product_name) {
            queryString = product_name
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/products/" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a product
    // ****************************************

    $("#delete-btn").click(function () {

        var product_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/products/" + product_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("product has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a product
    // ****************************************

    $("#search-btn").click(function () {

        var id=$("#product_id").val();
        var name = $("#product_name").val();
        var category = $("#product_category").val();
        var amount = $("#product_amount").val();
        var likecount = $("#product_likecount").val();
        var status = $("#product_category").val();
        // var available = $("#product_available").val() == "true";

        var queryString = ""
        if (id){
            queryString += 'id=' + id
        }

        if (name) {
            if (queryString.length > 0) {
                queryString += '&name=' + name
            }else{
                queryString += 'name=' + name
            }
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (amount) {
            if (queryString.length > 0) {
                queryString += '&amount=' + name
            }else{
                queryString += 'amount=' + name
            }
        }
        if (likecount) {
            if (queryString.length > 0) {
                queryString += '&likecount=' + name
            }else{
                queryString += 'likecount=' + name
            }
        }
        if (status) {
            if (queryString.length > 0) {
                queryString += '&status=' + status
            }else{
                queryString += 'status=' + status
            }
            }
            
        
        
        // if (available) {
        //     if (queryString.length > 0) {
        //         queryString += '&available=' + available
        //     } else {
        //         queryString += 'available=' + available
        //     }
        // }

        searchurl="/products?" + queryString
        if (queryString==('name='+name)){
            searchurl="/products/" + name
        }

        var ajax = $.ajax({
            type: "GET",
            url: searchurl,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:40%">Amount</th>'
            header += '<th style="width:40%">Likecount</th>'
            header += '<th style="width:40%">Status</th>'
            // header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            var firstProduct = "";
            for(var i = 0; i < res.length; i++) {
                var product = res[i];
                // var row = "<tr><td>"+product._id+"</td><td>"+product.name+"</td><td>"+product.category+"</td><td>"+product.available+"</td></tr>";
                var row = "<tr><td>"+product.id+"</td><td>"+product.name+"</td><td>"+product.category+"</td><td>"+product.amount+"</td><td>"+product.likecount+"</td><td>"+product.status+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstProduct = product;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
