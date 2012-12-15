# coding: utf8

def _handle_entry_chage(form):
    import string
    old_tags = set(row.tag for row in db(db.tags.entry==form.vars.id).select(db.tags.tag))
    new_tags = set(part[1:].rstrip(string.punctuation).lower() for part in form.vars.body.split() if part.startswith('#') and len(part)>1)
    
    #remove old tags
    for tag in old_tags - new_tags:
        db((db.tags.tag == tag) & (db.tags.entry == form.vars.id)).delete()
    
    #add new tags
    for tag in new_tags - old_tags:
        db.tags.insert(tag=tag, entry=form.vars.id)
        
    #TODO Handle Delete


# try something like
def index():
    return dict(entries=db(db.entry.id>0).select())

def new():
    return dict(form=crud.create(db.entry, onaccept=_handle_entry_chage))

def update():
    return dict(form=crud.update(db.entry, request.args(0), onaccept=(auth.archive,_handle_entry_chage) ))
    
def view():
    return dict(entry=db.entry[request.args(0)])

def view_history():
    return dict(history=db(db.entry_archive.current_record == request.args(0)).select(orderby=db.entry_archive.modified_on))
    
def tags():
    if len(request.args):
        return dict(entry=db((db.tags.tag==request.args(0)) & (db.tags.entry == db.entry.id)).select(db.entry.ALL))
    else:
        return dict(tags=db(db.tags.id>0).select(db.tags.tag, groupby=db.tags.tag))
