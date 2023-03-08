
# ActionLearning Week - SMS & Exam Engine

Our model focuses on building user-friendly, reliable, faster, and more efficient applications. We have developed a web application that avoids the need for any installation, making it easily accessible to users. The application provides a smooth transaction between the user and the application, making it a perfect fit for the educational industry.

## Project Description
The primary aim of this project is to provide a solution for schools to reduce paperwork and files, making tasks easier for staff and administrators. Our application is designed to enable parents to communicate with teachers without physically meeting them. The staff-related modules are simplified, and the application makes it easier to manage students, teachers, and other staff.

The staff module is designed to manage staff attendance, staff salary, etc. To access the staff-related module, the staff must be registered to the system. Students must also register to the system, and admission is assigned to the registered students. By using the admission number, students can pay their school fees via the system, and an auto-generated rated receipt will be printed.

Students can take MCQ online exams with the permission of the administrators. The fees module in the application is compatible with tuition fees and school fees. Users who are registered in the system can log in, but the accessibility will differ based on their role type, and the dashboard will be customized accordingly.

The final artifact will be a reusable prototype of the school management system. HTML, CSS, Bootstrap, Python Flask, jQuery, and sneat template have been used to develop the user interface of the school management system. Many microservices are built and integrated with the front-end design. The services provide an API that helps to bind with the front-end.

The project is developed considering the four main actors of the school management system. Multinomial naive Bayes theorem is used for the recommendation system for students. Previous data from the students are used to train the model, and NLTK library is used from Python for the feedback system. Stop Words are removed, so the model is not trained on common words. The data from the students are stored in the database and reused to train the model to improve efficiency.

## Microservices Architecture
The project follows a microservices architecture. The application is divided into several services that can be independently developed, deployed, and scaled. The services are:
- Authentication Service
- Staff Service
- Student Service
- Exam Service
- Fees Service
- Feedback Service
- Recommendation Service

Each service is designed to perform specific functions, and all services communicate with each other using APIs. The architecture is built on the principles of modularity, scalability, and fault-tolerance, making it easier to maintain and enhance the application.

## Conclusion
The ActionLearning Week project provides an efficient and effective solution to the challenges of school management. The microservices architecture makes it easier to develop, deploy, and scale the application, and the user-friendly interface makes it easier for users to interact with the application.
