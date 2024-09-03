-- Create unique index on users email
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Create index on transactions user_id for faster lookups
CREATE INDEX idx_transactions_user_id ON transactions(user_id);

-- Create index on budgets user_id for better performance
CREATE INDEX idx_budgets_user_id ON budgets(user_id);

-- Create index on transactions category_id for efficient querying
CREATE INDEX idx_transactions_category_id ON transactions(category_id);

-- Function to update the updated_at column
CREATE OR REPLACE FUNCTION set_updated_at_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for updating updated_at on users
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE PROCEDURE set_updated_at_timestamp();

-- Trigger for updating updated_at on categories
CREATE TRIGGER update_categories_updated_at
BEFORE UPDATE ON categories
FOR EACH ROW
EXECUTE PROCEDURE set_updated_at_timestamp();

-- Trigger for updating updated_at on transactions
CREATE TRIGGER update_transactions_updated_at
BEFORE UPDATE ON transactions
FOR EACH ROW
EXECUTE PROCEDURE set_updated_at_timestamp();

-- Trigger for updating updated_at on budgets
CREATE TRIGGER update_budgets_updated_at
BEFORE UPDATE ON budgets
FOR EACH ROW
EXECUTE PROCEDURE set_updated_at_timestamp();

-- Trigger for updating updated_at on notifications
CREATE TRIGGER update_notifications_updated_at
BEFORE UPDATE ON notifications
FOR EACH ROW
EXECUTE PROCEDURE set_updated_at_timestamp();