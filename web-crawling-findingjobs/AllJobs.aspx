<%@ Page Title="About" Language="C#" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="AllJobs.aspx.cs" Inherits="web_crawling_findingjobs.About" %>

<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">
    <style>
        .grid-container {
            padding: 15px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
    <!-- Data Sources -->
    <asp:ObjectDataSource runat="server"
        ID="odsJobs"
        SelectMethod="SellectALL"
        TypeName="web_crawling_findingjobs.JobListLogic.JobUtils.JobUtilities">
    </asp:ObjectDataSource>
    <!-- UI Components -->
    <h1>IT Job Listing in Saskatchewan</h1>
    <p>This is the entire job collection....some explanation</p>
    <div class="grid-container" ID="Main">
        <asp:GridView ID="grdJobs" runat="server" AutoGenerateColumns="False" DataSourceID="odsJobs">

            <Columns>
                <asp:BoundField DataField="Id" HeaderText="Id" SortExpression="Id"></asp:BoundField>
                <asp:BoundField DataField="CompanyName" HeaderText="CompanyName" SortExpression="CompanyName"></asp:BoundField>
                <asp:BoundField DataField="JobTitle" HeaderText="JobTitle" SortExpression="JobTitle"></asp:BoundField>
                <asp:BoundField DataField="Location" HeaderText="Location" SortExpression="Location"></asp:BoundField>
                <asp:BoundField DataField="Category" HeaderText="Category" SortExpression="Category"></asp:BoundField>
                <asp:BoundField DataField="Skills" HeaderText="Skills" SortExpression="Skills"></asp:BoundField>
                <asp:BoundField DataField="Years" HeaderText="Years" SortExpression="Years"></asp:BoundField>
                <asp:BoundField DataField="CitizePR" HeaderText="CitizePR" SortExpression="CitizePR"></asp:BoundField>
                <%--add Target="_blank for opening in a new tab after click--%>
                <asp:HyperLinkField DataNavigateUrlFields="Link" DataTextField="Link" Target="_blank" HeaderText="Link"></asp:HyperLinkField>

            </Columns>
        </asp:GridView>
    </div>
    <h2>Just some random pop up</h2>
    <div class="grid-container" ID="Random">
        <asp:Timer ID="timerRandomJob" runat="server" Interval="10000" OnTick="timerRandomJob_Tick"></asp:Timer>
        <!-- the timer is going to drive the updatepanel, so there is a trigger in the update panel that control by the timer ID -->
        <asp:UpdatePanel ID="updatePanelRandomJob" runat="server">
            <Triggers>
                <asp:AsyncPostBackTrigger ControlID="timerRandomJob" />
            </Triggers>
            <ContentTemplate>
                <!-- Data source for the random grid -->
                <asp:ObjectDataSource ID="odjJobsRandom" runat="server"
                    SelectMethod="SellectRandomJob" 
                    TypeName="web_crawling_findingjobs.JobListLogic.JobUtils.JobUtilities">
                </asp:ObjectDataSource>
                <asp:GridView ID="grdRandomJob" 
                    runat="server" 
                    AutoGenerateColumns="False"
                    DataSourceID="odjJobsRandom">
                    <Columns>
                        <asp:BoundField DataField="Id" HeaderText="Id" SortExpression="Id"></asp:BoundField>
                        <asp:BoundField DataField="CompanyName" HeaderText="CompanyName" SortExpression="CompanyName"></asp:BoundField>
                        <asp:BoundField DataField="JobTitle" HeaderText="JobTitle" SortExpression="JobTitle"></asp:BoundField>
                        <asp:BoundField DataField="Location" HeaderText="Location" SortExpression="Location"></asp:BoundField>
                        <asp:BoundField DataField="Skills" HeaderText="Skills" SortExpression="Skills"></asp:BoundField>
                        <asp:BoundField DataField="Years" HeaderText="Years" SortExpression="Years"></asp:BoundField>
                        <asp:BoundField DataField="Category" HeaderText="Category" SortExpression="Category"></asp:BoundField>
                        <asp:BoundField DataField="CitizePR" HeaderText="CitizePR" SortExpression="CitizePR"></asp:BoundField>
                        <asp:HyperLinkField DataNavigateUrlFields="Link" DataTextField="Link" Target="_blank" HeaderText="Link"></asp:HyperLinkField>
                    </Columns>
                </asp:GridView>
            </ContentTemplate>
        </asp:UpdatePanel>
    </div>
</asp:Content>
