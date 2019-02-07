import discord
import asyncio


class AuditManager:

    # TODO: Remove asyncio.sleep() When there is a new way to get audit logs.
    @staticmethod
    async def get_audit_log(guild, action: discord.AuditLogAction, target=None) -> discord.AuditLogEntry:
        await asyncio.sleep(0.5)
        if not target:
            async for entry in guild.audit_logs(limit=1, action=action):
                return entry
        else:
            async for entry in guild.audit_logs(action=action):
                if entry.target.id == target.id:
                    return entry

    # TODO: Remove asyncio.sleep() When there is a new way to get audit logs.
    @staticmethod
    async def get_last_audit_entry(guild) -> discord.AuditLogEntry:
        await asyncio.sleep(0.5)
        async for entry in guild.audit_logs(limit=1):
            return entry

    @staticmethod
    async def get_last_log_user(guild) -> discord.Member:
        entry = await AuditManager.get_last_audit_entry(guild)
        return entry.user

    @staticmethod
    async def get_last_audit_action(guild) -> discord.AuditLogAction:
        entry = await AuditManager.get_last_audit_entry(guild)
        return entry.action
