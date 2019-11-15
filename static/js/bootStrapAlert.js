bootstrap_alert = function() {}
bootstrap_alert.warning = function(message) {
	$('#modal-window').html('<div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true" id="alert-modal"><div class="modal-dialog" role="document"> <div class="modal-content"> <div class="modal-header">  <button type="button" class="close" data-dismiss="modal" aria-label="Закрыть"> <span aria-hidden="true">&times;</span> </button> </div> <div class="modal-body">' + message + ' </div> <div class="modal-footer"> <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button> </div> </div> </div> </div>');
	$('#alert-modal').modal('show');
}