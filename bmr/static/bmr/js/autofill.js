{
	$("#auto-batch").on("click", function(e) {
		e.preventDefault();
		 var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
            	if (data.message) {
            		$("#messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
            	} else {
            		$('body').html(data.form)
            	}
                
            }
        })
	})

    $("#auto-batch-info").on("click", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#autofill-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $('body').html(data.form)
                }
                
            }
        })
    })

    $("#auto-guide").on("click", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#guide-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $('body').html(data.form)
                }
                
            }
        })
    })

    $("#auto-eq-check").on("click", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#eq-autofill").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $('body').html(data.form)
                }
                
            }
        })
    })

   $("#auto-eq-clear").on("click", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#clearance-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $('body').html(data.form)
                }
                
            }
        })
    })

  $("#auto-raw-bill").on("click", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#rw-bill-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $('body').html(data.form)
                }
                
            }
        })
    })

    $("#auto-batch-process").on("click", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#process-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $('body').html(data.form)
                }
                
            }
        })
    })

    $("#auto-raw-check").on("click", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#raw-check-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $('body').html(data.form)
                }
                
            }
        })
    })

    $("#auto-process-control").on("click", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#batch-process-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $("#autofill-body").html(data.form)
                }
                
            }
        })
    })

    $("#auto-clean").on("click", function(e) {
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#clean-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $("#autofill-clean-body").html(data.form)
                }
                
            }
        })
    })


    $("#auto-qc").on("click", function(e) {
        console.log(e);
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#qc-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $("body").html(data.form)
                }
                
            }
        })
    })

    $("#auto-yield").on("click", function(e) {
        console.log(e);
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#yield-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $("body").html(data.form)
                }
                
            }
        })
    })

    $("#auto-sample").on("click", function(e) {
        console.log(e);
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#sample-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $("body").html(data.form)
                }
                
            }
        })
    })

    $("#auto-recon-pack").on("click", function(e) {
        console.log(e);
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#recon-pack-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $("body").html(data.form)
                }
                
            }
        })
    })

    $("#auto-release").on("click", function(e) {
        console.log(e);
        e.preventDefault();
        var btn = $(this)
        $.ajax({
            url: btn.attr("target"),
            type: "GET",
            dataType: "json",
            success: function(data) {
                if (data.message) {
                    $("#release-messages").append(`<div class='text-center alert alert-danger'>${data.message}</div>`);
                } else {
                    $("body").html(data.form)
                }
                
            }
        })
    })
}