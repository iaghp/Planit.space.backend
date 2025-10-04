import snowflake from 'snowflake-sdk';
import 'dotenv/config';

// Create a Connection object that we can use later to connect.
const connection = snowflake.createConnection({
    account: process.env.SNOWFLAKE_ACCOUNT,
    username: process.env.SNOWFLAKE_USER,
    password: process.env.SNOWFLAKE_PASSWORD,
    application: process.env.SNOWFLAKE_APPLICATION,
    role: process.env.SNOWFLAKE_ROLE,
    warehouse: process.env.SNOWFLAKE_WAREHOUSE,   // e.g. 'COMPUTE_WH'
    database: process.env.SNOWFLAKE_DATABASE,   
  });
// Try to connect to Snowflake, and check whether the connection was successful.
connection.connect( 
    function(err, conn) {
        if (err) {
            console.error('Unable to connect: ' + err.message);
            } 
        else {
            console.log('Successfully connected to Snowflake.');
            // Optional: store the connection ID.
            connection_ID = conn.getId();
            console.log(`Connection id: ${connection_ID}`)
            }
    }
);

// Create the connection pool instance
const connectionPool = snowflake.createPool(
    // connection options
    {
        account: process.env.SNOWFLAKE_ACCOUNT,
        username: process.env.SNOWFLAKE_USER,
        password: process.env.SNOWFLAKE_PASSWORD,
        role: process.env.SNOWFLAKE_ROLE,
        warehouse: process.env.SNOWFLAKE_WAREHOUSE,   // e.g. 'COMPUTE_WH'
        database: process.env.SNOWFLAKE_DATABASE, 
        schema: process.env.SNOWFLAKE_SCHEMA  
    },
    // pool options
    {
      max: 10, // specifies the maximum number of connections in the pool
      min: 0   // specifies the minimum number of connections in the pool
    }
);

export const query = async(stmt, vars = [], then = () => {}) => {
    console.log(stmt)
    console.log(vars)
    connectionPool.use(async (clientConnection) => {
        const statement = await clientConnection.execute({
            sqlText: stmt,
            binds: vars,
            complete: function (err, stmt, rows)
            {   
                const consumedRows = []
                var stream = stmt.streamRows();
                stream.on('data', function (row)
                {
                    console.log(row);
                    consumedRows.push(row)
                });
                stream.on('end', function (row)
                {
                    console.log('All rows consumed');
                    console.log(consumedRows)
                    then(consumedRows)
                });
            }
        })
    })
}