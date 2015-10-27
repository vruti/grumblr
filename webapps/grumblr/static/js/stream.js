function getPosts() {
	//Get the last post ID
	var posts = $(".postStream .post");
	var post = posts.first();
	var postID = post.attr("id");
	if(postID == undefined) postID = 0;
	//Get all new posts so only new posts
	//are added to stream
	console.log(postID);
	  $.ajax({
		 url: '/grumblr/get-posts/' + postID,
		 type: "GET",
		 dataType: "json",
		 success: function(resp) {
			 $(".posts").prepend(resp);
			 console.log("Done");
		 }
	  });
}

$(document).ready(function () {
  // Set up to-do list with initial DB items and DOM data
  getPosts();

  // Periodically refresh to-do list
  window.setInterval(getPosts, 5000);
});
