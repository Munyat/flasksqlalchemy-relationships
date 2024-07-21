from app import app, db
from app import Member, Order, Course, user_courses
from datetime import date
from faker import Faker

fake = Faker()

with app.app_context():
        # Drop all existing data
        db.session.query(Order).delete()
        db.session.query(Member).delete()
        db.session.query(Course).delete()
        db.session.query(user_courses).delete()
        
        # Commit the deletions
        db.session.commit()

        # Number of members and orders to create
        num_members = 10
        num_courses = 5
        num_orders_per_member = 5

        # Create courses
        courses = [Course(name=fake.word()) for _ in range(num_courses)]
        db.session.bulk_save_objects(courses)
        db.session.commit()

        for _ in range(num_members):
            member = Member(
                username=fake.user_name(),
                password="password",
                email=fake.email(),
                join_date=date.today()
            )
            db.session.add(member)
            db.session.flush()  # Flush to get the member id before adding courses
            
            # Create orders for each member
            for _ in range(num_orders_per_member):
                order = Order(
                price=fake.random_number(digits=5),
                member_id=member.id
                )
                db.session.add(order)
                # member.orders.append(order)


            # Fetch all courses
            all_courses = Course.query.all()
            
            # Get a unique subset of courses to add to the member
            unique_courses = set(fake.random_elements(elements=all_courses, length=fake.random_int(min=1, max=num_courses), unique=True))
            
            # Add unique courses to the member
            for course in unique_courses:
                if course not in member.courses:
                    member.courses.append(course)

        # Commit the session to the database
        db.session.commit()
