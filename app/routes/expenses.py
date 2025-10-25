import datetime
from flask import Blueprint, request, jsonify
from app.models import Expense, db

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/expenses', methods=['POST'])
def create_expense():
    """
    Create a new expense entry.
    ---
    tags:
      - Expenses
    parameters:
      - in: body
        name: body
        required: true
        schema: 
            type: object
            properties:
                title:
                    type: string
                    example: "Lunch"
                amount:
                    type: number
                    example: 15.50
                description:
                    type: string
                    example: "Lunch with colleagues"
                date:
                    type: string
                    example: "2024-06-15"
    responses:
      201:
        description: Expense created successfully.
        schema:
            type: object
            properties:
                message:
                    type: string
                    example: "Expense created successfully."
                expense:
                    type: object
                    properties:
                        id:
                            type: integer
                            example: 1
                        title:
                            type: string            
                            example: "Lunch"
                        amount:
                            type: number
                            example: 15.50
                        description:
                            type: string
                            example: "Lunch with colleagues"
                        date:
                            type: string
                            example: "2024-06-15"
                        user_id:
                            type: integer
                            example: 1
      400:
        description: Invalid input data.
        schema:
            type: object
            properties:
                message:
                    type: string
                    example: "Title, amount, and date are required fields."
    """
    data = request.get_json()
    
    title = data.get('title')
    amount = data.get('amount')
    description = data.get('description')
    date = data.get('date')
    user_id = data.get('user_id')

    if not title or not amount or not date or not user_id:
        return jsonify({'message': 'Title, amount, date, and user_id are required fields.'}), 400

    new_expense = Expense(
        title=title, 
        amount=amount, 
        description=description, 
        date=date,
        user=user_id
        
    )
    
    db.session.add(new_expense)
    db.session.commit()

    just_created_expense =  Expense.query.get(new_expense.id)

    return jsonify({
        'message': 'Expense created successfully.',
        'expense': {
            'id': just_created_expense.id,
            'title': just_created_expense.title,
            'amount': just_created_expense.amount,
            'description': just_created_expense.description,
            'date': just_created_expense.date,
            'user_id': just_created_expense.user
        }
    }), 201

   
    
@expenses_bp.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    """
    Retrieve an expense by its ID.
    ---
    tags:
      - Expenses
    parameters:
      - in: path
        name: expense_id
        required: true
        type: integer
        description: The ID of the expense to retrieve.
    responses:
      200:
        description: Expense retrieved successfully.
        schema:
            type: object
            properties:
                id:
                    type: integer
                    example: 1
                title:
                    type: string            
                    example: "Lunch"
                amount:
                    type: number
                    example: 15.50
                description:
                    type: string    
                    example: "Lunch with colleagues"
                date:
                    type: string
                    example: "2024-06-15"
                user_id:
                    type: integer
                    example: 1
      404:
        description: Expense not found.
        schema:
            type: object
            properties:
                message:
                    type: string
                    example: "Expense not found."   
    """
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'message': 'Expense not found.'}), 404
    return jsonify({
        'id': expense.id,
        'title': expense.title,
        'amount': expense.amount,
        'description': expense.description,
        'date': expense.date,
        'user_id': expense.user
    })

@expenses_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """
    Update an existing expense.
    ---
    tags:
      - Expenses
    parameters:
      - in: path
        name: expense_id
        required: true
        type: integer
        description: The ID of the expense to update.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
                example: "Lunch"
              amount:
                type: number
                example: 15.50
              description:
                type: string
                example: "Lunch with colleagues"
              date:
                type: string
                example: "2024-06-15"
    responses:
      200:
        description: Expense updated successfully.
        schema:
            type: object
            properties:
                id:
                    type: integer
                    example: 1
                title:
                    type: string
                    example: "Lunch"
                amount:
                    type: number
                    example: 15.50
                description:
                    type: string
                    example: "Lunch with colleagues"
                date:
                    type: string
                    example: "2024-06-15"
                user_id:
                    type: integer
                    example: 1
      404:
        description: Expense not found.
        schema:
            type: object
            properties:
                message:
                    type: string
                    example: "Expense not found."
    """
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'message': 'Expense not found.'}), 404

    data = request.get_json()
    expense.title = data.get('title', expense.title)
    expense.amount = data.get('amount', expense.amount)
    expense.description = data.get('description', expense.description)
    expense.date = data.get('date', expense.date)
    expense.user = data.get('user_id', expense.user)

    db.session.add(expense)
    db.session.commit()

    return jsonify({
        'id': expense.id,
        'title': expense.title,
        'amount': expense.amount,
        'description': expense.description,
        'date': expense.date,
        'user_id': expense.user
    })

@expenses_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """
    Delete an expense by its ID.
    ---
    tags:
      - Expenses
    parameters:
      - in: path
        name: expense_id
        required: true
        type: integer
        description: The ID of the expense to delete.
    responses:
        200:            
            description: Expense deleted successfully.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Expense deleted successfully."
        404:
            description: Expense not found.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Expense not found."
    """
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'message': 'Expense not found.'}), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({'message': 'Expense deleted successfully.'})