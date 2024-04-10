db = db.getSiblingDB('restaurant');
db.createUser({
  user: 'mongoUser',
  pwd: 'dd74d6aecd2a6ebb0',
  roles: [
    {
      role: 'readWrite',
      db: 'restaurant'
    }
  ]
});

db.tables.createIndex({ "table_number": 1 }, { unique: true });
