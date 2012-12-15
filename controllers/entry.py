# coding: utf8

def _handle_entry_chage(form):
    import string
    old_tags = set(row.tag for row in db(db.tags.entry==form.vars.id).select(db.tags.tag))
    new_tags = set(part[1:].rstrip(string.punctuation).lower() for part in MARKMIN(form.vars.body).xml().split() if part.startswith('#') and len(part)>1)
    
    #remove old tags
    for tag in old_tags - new_tags:
        db((db.tags.tag == tag) & (db.tags.entry == form.vars.id)).delete()
    
    #add new tags
    for tag in new_tags - old_tags:
        db.tags.insert(tag=tag, entry=form.vars.id)
        
    #TODO Handle Delete


# try something like
def index():
    return dict(entries=db(db.entry.id>0).select(orderby=~db.entry.created_on))

@auth.requires_login()
def new():
    return dict(form=crud.create(db.entry, onaccept=_handle_entry_chage))

@auth.requires_login()
def update():
    return dict(form=crud.update(db.entry, request.args(0), \
    onaccept=(auth.archive,_handle_entry_chage), next=URL("entry","view",args=request.args(0))))
    
def view():
    row = db((db.entry.id == request.args(0)) & (db.entry.created_by == db.auth_user.id)).select(
        db.entry.ALL, db.auth_user.first_name, db.auth_user.last_name).first()
    return dict(entry=row.entry, author=row.auth_user)

def view_history():
    return dict(history=db(db.entry_archive.current_record == request.args(0)).select(orderby=db.entry_archive.modified_on))
    
def tags():
    if len(request.args):
        return dict(entry=db((db.tags.tag==request.args(0)) & (db.tags.entry == db.entry.id)).select(db.entry.ALL))
    else:
        tags = []
        for row in db(db.tags.id>0).select(db.tags.tag, db.tags.tag.count(), groupby=db.tags.tag):
            tags.append({'tag':row.tags.tag, 'count':row['_extra']['COUNT(tags.tag)']})
        
        return dict(tags=tags)
