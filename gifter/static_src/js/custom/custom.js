/**
 * This file is part of Shoop Gifter Demo.
 *
 * Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
 *
 * This source code is licensed under the AGPLv3 license found in the
 * LICENSE file in the root directory of this source tree.
 */

function updatePrice() {
    var $quantity = $("#product-quantity");
    if ($quantity.length === 0 || !$quantity.is(":valid")) {
        return;
    }

    var data = {
        id: $("input[name=product_id]").val(),
        quantity: $quantity.val()
    };
    var $simpleVariationSelect = $("#product-variations");
    if ($simpleVariationSelect.length > 0) {
        // Smells like a simple variation; use the selected child's ID instead.
        data.id = $simpleVariationSelect.val();
    } else {
        // See if we have variable variation select boxes; if we do, add those.
        $("select.variable-variation").serializeArray().forEach(function(obj) {
            data[obj.name] = obj.value;
        });
    }
    jQuery.ajax({url: "/xtheme/product_price", dataType: "html", data: data}).done(function(responseText) {
        var $content = jQuery("<div>").append(jQuery.parseHTML(responseText)).find("#product-price-div");
        jQuery("#product-price-div").replaceWith($content);
        if ($content.find("#no-price").length > 0) {
            $("#add-to-cart-button").prop("disabled", true);
        } else {
            $("#add-to-cart-button").not(".not-orderable").prop("disabled", false);
        }
    });
}


function openSideNav() {
    $(document.body).addClass("menu-open");
}

function closeSideNav() {
    $(document.body).removeClass("menu-open");
}

function sideNavIsOpen() {
    return $(document.body).hasClass("menu-open");
}

function openSideCart() {
    $(document.body).addClass("cart-open");
}

function closeSideCart() {
    $(document.body).removeClass("cart-open");
}

function sideCartIsOpen() {
    return $(document.body).hasClass("cart-open");
}

$(function() {

    $(document).on("change", ".variable-variation, #product-variations, #product-quantity", updatePrice);

    updatePrice();

    $(".toggle-side-nav").click(function(e) {
        e.stopPropagation();
        closeSideCart();
        if (sideNavIsOpen()) {
            closeSideNav();
        } else {
            openSideNav();
        }
    });

    $("#navigation-basket-partial").on("click", ".toggle-cart-nav", function(e) {
        e.stopPropagation();
        closeSideNav();
        if (sideCartIsOpen()) {
            closeSideCart();
        } else {
            openSideCart();
        }
    });

    $(".side-cart .scroll-inner-content").scrollbar();

    $(document).click(function(e) {
        if (sideNavIsOpen() && !$(e.target).closest(".side-nav").length) {
            closeSideNav();
        }
        if (sideCartIsOpen() && !$(e.target).closest(".side-cart").length) {
            closeSideCart();
        }
    });

    $(".top-nav .user-menu-button").click(function() {
        closeSideCart();
        closeSideNav();
    });

    $(".top-nav .dropdown-menu").click(function(e) {
        e.stopPropagation();
    });

    //add tooltip triggers to data-attribute html with data-toggle=tooltip
    $("[data-toggle='tooltip']").tooltip({
        delay: { "show": 750, "hide": 100 }
    });

    // Add slideDown animation to all bootstrap dropdowns
    $(".dropdown").on("show.bs.dropdown", function() {
        $(this).find(".dropdown-menu").first().stop(true, true).slideDown(200, "easeInSine");
    });

    // Add slideUp animation to all bootstrap dropdowns
    $(".dropdown").on("hide.bs.dropdown", function() {
        $(this).find(".dropdown-menu").first().stop(true, true).slideUp(300, "easeOutSine");
    });

    $(".selectpicker select").selectpicker();

});
