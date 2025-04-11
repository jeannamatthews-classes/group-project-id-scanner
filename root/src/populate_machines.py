from app import app
from tables import db, Machine

machine_names = [
    "Soldering Station",
    "Vinyl Station",
    "Laser Engravers",
    "Paint Station",
    "Woodworking",
    "Glass/Jewelry Station",
    "Print Your Own",
    "Misc Tools"
]

with app.app_context():
    for name in machine_names:
        #check if machine already exists
        existing = Machine.query.filter_by(name=name).first()
        if not existing:
            new_machine = Machine(name=name)
            db.session.add(new_machine)
            print(f"Adding machine: {name}")
        else:
            print(f"Machine already exists: {name}")
    
    #Commit changes to db
    db.session.commit()
    print("Machines table has been populated")