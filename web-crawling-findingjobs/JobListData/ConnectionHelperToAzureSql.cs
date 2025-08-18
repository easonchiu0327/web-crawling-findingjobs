using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data.SqlClient;
using System.Linq;
using System.Web;

namespace web_crawling_findingjobs.JobListData
{
    public class ConnectionHelperToAzureSql
    {
        public static string GetConnectionString()
        {
            // 1. Try to get connection string from environment variable (SQLDB_CONN).
            var fromEnv = Environment.GetEnvironmentVariable("SQLDB_CONN");
            // 2. If the environment variable is set and not empty, use it.
            if (!string.IsNullOrWhiteSpace(fromEnv))
                return fromEnv;

            // 3. Otherwise, fall back to Web.config.
            return ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;
        }

        public static SqlConnection GetConnection()
        {
            // Create a new SqlConnection using whichever connection string is returned above.
            // This way, calling code doesn’t have to worry about where the connection string comes from.
            return new SqlConnection(GetConnectionString());
        }
    }
}