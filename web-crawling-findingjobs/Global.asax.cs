using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data.SqlClient;
using System.Linq;
using System.Web;
using System.Web.Optimization;
using System.Web.Routing;
using System.Web.Security;
using System.Web.SessionState;
using web_crawling_findingjobs.JobListData;

namespace web_crawling_findingjobs
{
    public class Global : HttpApplication
    {
        void Application_Start(object sender, EventArgs e)
        {
            // Code that runs on application startup
            RouteConfig.RegisterRoutes(RouteTable.Routes);
            BundleConfig.RegisterBundles(BundleTable.Bundles);
        }

        //increment the counts once per visitor session
        protected void Session_Start(object sender, EventArgs e)
        {
            // Increment daily + total once for each new session
            const string sql = @"
MERGE dbo.VisitorStats AS target
USING (SELECT CAST(GETDATE() AS DATE) AS VisitDate) AS source
ON (target.VisitDate = source.VisitDate)
WHEN MATCHED THEN
    UPDATE SET 
        DailyVisitors = target.DailyVisitors + 1,
        TotalVisitors = target.TotalVisitors + 1
WHEN NOT MATCHED THEN
    INSERT (VisitDate, DailyVisitors, TotalVisitors)
    VALUES (
        source.VisitDate,
        1,
        (SELECT ISNULL(MAX(TotalVisitors), 0) + 1 FROM dbo.VisitorStats)
    );";

            using (var conn = ConnectionHelperToAzureSql.GetConnection())
            using (var cmd = new SqlCommand(sql, conn))
            {
                conn.Open();
                cmd.ExecuteNonQuery();
            }
        }
    }
}