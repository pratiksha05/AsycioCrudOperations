"""Used to perform Crud operations"""
import logging as logger
from aiohttp import web
from models.db import Agent, System


class AgentCrud(web.View):
    """Used to define HTTP methods"""

    async def post(self):
        """
        @description - Used to insert agent records.
        @param - self: post request with data to insert.
        @returns - response with status 200 in case of success and 500 in case of exception.
        """
        data = await self.request.json()
        register_date = data["register_date"]
        ip_address = data["ip_address"]
        try:
            Agent.create(register_date=register_date, ip_address=ip_address)
            response_obj = {"status": "success"}
            return web.Response(text=str(response_obj), status=201)
        except Exception as exception:
            response_obj = {"status": "failed", "reason": exception}
            error_message = str(exception)
            logger.error(error_message)
            return web.Response(text=str(response_obj), status=500)

    async def delete(self):
        """
        @description - Used to delete agent record
        @param - self: delete request with id to delete record.
        @returns - response with status 200 in case of success and 500 in case of exception.
        """
        try:
            data = await self.request.json()
            agent_uuid = data.get("agent_uuid")
            agent_to_delete = Agent.filter(Agent.uuid == agent_uuid).first()
            sys_id = (
                System.select().where(System.agent_uuid == agent_to_delete).execute()
            )
            if sys_id:
                logger.error("Agent not deleted")
                return web.Response(text="Agent not deleted.")
            else:
                agent_to_delete.delete_instance()
                logger.info("Agent deleted successfully")
            return web.Response(text="Agent deleted successfully.")
        except Exception as ex:
            error_message = str(ex)
            logger.error(error_message)
            return web.Response(text=error_message, status=500)

    async def get(self):
        """@param - self: request with URL:'/'
           @returns - response with success status.
        """
        data = self.request.match_info["uuid"]
        try:
            if data:
                agent = Agent.get(Agent.uuid == data)
                table = [agent.uuid, agent.ip_address, agent.register_date]
                logger.info("Data received!!!")
                return web.Response(body=str(table), status=200)
        except Exception as ex:
            error_message = str(ex)
            logger.error(error_message)
        return web.Response(text=error_message, status=500)

    async def put(self):
        """
        @description - Used to update agent record.
        @param - self: put request with id to update record and data to update.
        @returns - response with status 200 in case of success and 500 in case of exception.
        """
        data = await self.request.json()
        agent_uuid = data["agent_uuid"]
        ip_address = data["ip_address"]
        agent_obj = Agent.filter(Agent.uuid == agent_uuid).first()
        if not agent_obj:
            response_obj = {"status": "failed"}
            logger.error("No agent found!!!")
            return web.Response(text=str(response_obj), status=500)
        try:
            Agent.update(ip_address=ip_address).where(Agent.uuid == agent_uuid)
            logger.info("Agent updated!!!")
            return web.Response(text="successful", status=200)
        except Exception as ex:
            response_obj = {"status": "failed"}
            error_message = str(ex)
            logger.error(error_message)
            return web.Response(text=str(response_obj), status=500)


class SystemCrud(web.View):
    """Used to define HTTP methods"""

    async def post(self):
        """
        @description - Used to insert System records.
        @param - self: post request with data to insert.
        @returns - response with status 200 in case of success and 500 in case of exception.
        """

        data = await self.request.json()
        agent_uuid = data.get("agent_uuid")
        agent = Agent.get(Agent.uuid == agent_uuid)
        if not agent:
            response_obj = {"status": "failed", "reason": "agent not present"}
            logger.info("agent not present")
            return web.Response(text=str(response_obj), status=404)
        try:
            System.create(agent_uuid=agent)
            logger.info("System created successfully!!!")
            return web.Response(text="Successful", status=201)
        except Exception as ex:
            response_obj = {"status": "failed", "reason": "agent not added"}
            error_message = str(ex)
            logger.error(error_message)
            return web.Response(text=str(response_obj), status=500)

    async def get(self):
        """
        @description - Used to get System records.
        @param - self: Get request.
        @returns - response with status 200 in case of success and 404 in case of exception.
        """
        try:
            query = System.select().execute()
            table = []
            for facility in query:
                table.append(facility)
            return web.Response(body=str(table), status=200)
        except Exception as ex:
            error_message = str(ex)
            logger.error(error_message)
            return web.Response(text=str(error_message), status=404)

    async def delete(self):
        """
        @description - Used to delete system record
        @param - self: delete request with id to delete record.
        @returns - response with status 200 in case of success and 500 in case of exception.
        """

        data = await self.request.json()
        system_uuid = data.get("sys_id")
        sys_del = System.get(System.uuid == system_uuid)
        if not sys_del:
            response_obj = {"status": "failed", "reason": "System not Present"}
            return web.Response(text=str(response_obj), status=500)
        try:
            sys_del.delete_instance()
            logger.info("System deleted successfully!!!")
            return web.Response(text="Successful", status=200)
        except Exception as ex:
            response_obj = {"status": "failed", "reason": str(ex)}
            error_message = str(ex)
            logger.error(error_message)
            return web.Response(text=str(response_obj), status=500)
