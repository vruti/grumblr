//Gets all new comments or all comments if view comments is clicked on
function getComments(event) {
	console.log("getting comments");
	var postid = $(this).attr('post-id');
	console.log(postid);
	$.ajax({type: "GET",
			dataType: "json",
			url: "/grumblr/get-comments/" + postid,
			success: function(resp) {
				$(".commentList" + postid).empty()
				console.log(this);
				$.each(resp, function() {
					var commentBlock = 	'<li>' +
                    	this["comment"] + '</li>';
					$(".commentList" + postid).append(commentBlock);
				});
			},
	});
}

//Adds a new comment and displays it
function addComment(e) {
	e.preventDefault();
	var postid = $(this).attr("post-id");
	console.log(postid);
	var form = $("#commentForm" + postid);
	$.ajax({
		url: '/grumblr/add-comment/' + postid,
		type: "POST",
		dataType: "json",
		data: form.serialize(),
		success: function(resp) {
			console.log("adding comment");
			$(".commentList" + postid).empty();
			console.log(this)
			$.each(resp, function() {
				console.log(this["comment"]);
				var commentBlock = 	'<li>' +
                    	this["comment"] + '</li>';			
					$(".commentList" + postid).append(commentBlock);
				});
			form.trigger("reset");
			console.log("done");
		}
	});
	
}

$(document).ready(function () {
  // Set up to-do list with initial DB items and DOM data
  console.log("hi");
  $(".addComment").on("click", addComment);
  $(".getComments").on("click", getComments);
});
