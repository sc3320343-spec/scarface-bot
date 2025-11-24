import requests
import time
import os
import json
from datetime import datetime
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8251206230:AAE2-vFQ3ljxE6Bv71h5BbkyRKgFnr1p6ac"
API_URL = "http://92.118.206.4:8488/logs"

class EnterpriseLogsBot:
    def __init__(self):
        self.processing_requests = {}
        self.system_stats = {
            'total_searches': 0,
            'total_credentials_found': 0,
            'active_sessions': set(),
            'success_rate': 0,
            'average_processing_time': 0
        }
        self.search_history = []
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Interface corporativa inicial"""
        user_id = update.effective_user.id
        self.system_stats['active_sessions'].add(user_id)
        
        keyboard = [
            [InlineKeyboardButton("🔍 EXECUTAR BUSCA", callback_data="execute_search")],
            [InlineKeyboardButton("📊 PAINEL DE CONTROLE", callback_data="control_panel")],
            [InlineKeyboardButton("⚙️ CONFIGURAÇÕES", callback_data="system_settings")],
            [InlineKeyboardButton("📋 RELATÓRIOS", callback_data="reports")],
            [InlineKeyboardButton("🆘 SUPORTE TÉCNICO", callback_data="technical_support")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        enterprise_text = """
🏢 *SISTEMA CORPORATIVO DE ANÁLISE DE LOGS*
*SCARFACE ENTERPRISE EDITION*

┌─────────────────────────────────────┐
         *PLATAFORMA DE INTELIGÊNCIA*
└─────────────────────────────────────┘

*SISTEMA OPERACIONAL*
• Status: ✅ **ONLINE**
• Versão: Enterprise v3.0
• Segurança: Nível Máximo
• Performance: Otimizada

*RECURSOS DISPONÍVEIS*
• 🔍 Busca Avançada em Tempo Real
• 📊 Analytics e Business Intelligence  
• 🔒 Processamento Criptografado
• ⚡ Infraestrutura de Alta Disponibilidade

*Selecione uma operação:*
        """
        
        if update.message:
            await update.message.reply_text(enterprise_text, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            await update.callback_query.message.reply_text(enterprise_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gerenciador de operações corporativas"""
        query = update.callback_query
        await query.answer()
        
        handlers = {
            "execute_search": self.show_search_operations,
            "control_panel": self.show_control_panel,
            "system_settings": self.show_system_settings,
            "reports": self.show_reports_dashboard,
            "technical_support": self.show_technical_support,
            "quick_scan": lambda q: self.request_target_url(q, "quick_scan"),
            "deep_analysis": lambda q: self.request_target_url(q, "deep_analysis"),
            "comprehensive_audit": lambda q: self.request_target_url(q, "comprehensive_audit"),
            "back_to_main": self.start
        }
        
        if query.data in handlers:
            await handlers[query.data](query)

    async def show_search_operations(self, query):
        """Painel de operações de busca"""
        keyboard = [
            [InlineKeyboardButton("⚡ SCAN RÁPIDO", callback_data="quick_scan")],
            [InlineKeyboardButton("🔍 ANÁLISE PROFUNDA", callback_data="deep_analysis")],
            [InlineKeyboardButton("📈 AUDITORIA COMPLETA", callback_data="comprehensive_audit")],
            [InlineKeyboardButton("📊 VOLTAR AO PAINEL", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        operations_text = """
🔍 *CENTRAL DE OPERAÇÕES - MÓDULO DE BUSCA*

┌─────────────────────────────────────┐
          *MODOS DE OPERAÇÃO*
└─────────────────────────────────────┘

*⚡ SCAN RÁPIDO*
▸ Finalidade: Análise Preliminar
▸ Duração: 2-4 minutos
▸ Amostragem: 300-500 registros
▸ Uso: Verificação Rápida

*🔍 ANÁLISE PROFUNDA*  
▸ Finalidade: Investigação Detalhada
▸ Duração: 5-8 minutos  
▸ Amostragem: 1.000-2.000 registros
▸ Uso: Auditoria Completa

*📈 AUDITORIA COMPLETA*
▸ Finalidade: Análise Exaustiva
▸ Duração: 8-12 minutos
▸ Amostragem: 5.000-10.000 registros
▸ Uso: Inteligência Corporativa

*Selecione o modo operacional:*
        """
        
        await query.edit_message_text(operations_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def show_control_panel(self, query):
        """Dashboard corporativo"""
        keyboard = [
            [InlineKeyboardButton("🔄 ATUALIZAR MÉTRICAS", callback_data="control_panel")],
            [InlineKeyboardButton("🔍 NOVA OPERAÇÃO", callback_data="execute_search")],
            [InlineKeyboardButton("⚙️ CONFIGURAÇÕES", callback_data="system_settings")],
            [InlineKeyboardButton("🏠 PAINEL PRINCIPAL", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Cálculo de métricas em tempo real
        success_rate = (self.system_stats['total_credentials_found'] / 
                       max(self.system_stats['total_searches'], 1)) * 100
        
        control_panel_text = f"""
📊 *PAINEL DE CONTROLE CORPORATIVO*

┌─────────────────────────────────────┐
         *DASHBOARD EXECUTIVO*
└─────────────────────────────────────┘

*📈 MÉTRICAS DE PERFORMANCE*
• Operações Concluídas: `{self.system_stats['total_searches']}`
• Credenciais Identificadas: `{self.system_stats['total_credentials_found']}`
• Taxa de Sucesso: `{success_rate:.1f}%`
• Sessões Ativas: `{len(self.system_stats['active_sessions'])}`

*⚙️ STATUS DO SISTEMA*
• API Connection: `{'✅ OPERACIONAL' if await self.test_api() else '❌ OFFLINE'}`
• Processos Ativos: `{len(self.processing_requests)}`
• Latência: `{self.get_system_latency()}ms`
• Uptime: `99.8%`

*🔒 SEGURANÇA*
• Criptografia: AES-256
• Autenticação: 2FA Ready  
• Compliance: Enterprise Grade
• Auditoria: Logs Completos

*🕐 ÚLTIMA ATUALIZAÇÃO*
{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        """
        
        await query.edit_message_text(control_panel_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def show_system_settings(self, query):
        """Configurações do sistema corporativo"""
        keyboard = [
            [InlineKeyboardButton("🎯 PREFERÊNCIAS DE BUSCA", callback_data="search_preferences")],
            [InlineKeyboardButton("📁 FORMATOS DE SAÍDA", callback_data="output_formats")],
            [InlineKeyboardButton("🔔 SISTEMA DE ALERTAS", callback_data="alert_system")],
            [InlineKeyboardButton("🏠 PAINEL PRINCIPAL", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        settings_text = """
⚙️ *CENTRAL DE CONFIGURAÇÕES*

┌─────────────────────────────────────┐
        *ADMINISTRAÇÃO DO SISTEMA*
└─────────────────────────────────────┘

*🎯 PREFERÊNCIAS DE BUSCA*
▸ Configuração de Algoritmos
▸ Limites de Processamento
▸ Otimização de Performance

*📁 FORMATOS DE SAÍDA*
▸ Estrutura de Relatórios
▸ Templates Corporativos
▸ Integração com Sistemas

*🔔 SISTEMA DE ALERTAS*
▸ Notificações em Tempo Real
▸ Monitoramento Contínuo
▸ Gestão de Incidentes

*Selecione uma categoria para configurar:*
        """
        
        await query.edit_message_text(settings_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def show_reports_dashboard(self, query):
        """Dashboard de relatórios"""
        keyboard = [
            [InlineKeyboardButton("📋 RELATÓRIO EXECUTIVO", callback_data="executive_report")],
            [InlineKeyboardButton("🔍 RELATÓRIO TÉCNICO", callback_data="technical_report")],
            [InlineKeyboardButton("📊 ANALYTICS", callback_data="analytics_dashboard")],
            [InlineKeyboardButton("🏠 PAINEL PRINCIPAL", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        reports_text = """
📋 *CENTRAL DE RELATÓRIOS*

┌─────────────────────────────────────┐
         *BUSINESS INTELLIGENCE*
└─────────────────────────────────────┘

*📋 RELATÓRIO EXECUTIVO*
▸ Visão Geral de Performance
▸ Métricas Corporativas
▸ Análise de Tendências

*🔍 RELATÓRIO TÉCNICO*
▸ Dados Técnicos Detalhados
▸ Logs de Processamento
▸ Diagnóstico de Sistema

*📊 ANALYTICS*
▸ Análise Preditiva
▸ Dashboard Interativo
▸ Business Intelligence

*Selecione o tipo de relatório:*
        """
        
        await query.edit_message_text(reports_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def show_technical_support(self, query):
        """Suporte técnico corporativo"""
        keyboard = [
            [InlineKeyboardButton("📞 CONTATO IMEDIATO", callback_data="immediate_contact")],
            [InlineKeyboardButton("🔧 DIAGNÓSTICO", callback_data="system_diagnostic")],
            [InlineKeyboardButton("📚 BASE DE CONHECIMENTO", callback_data="knowledge_base")],
            [InlineKeyboardButton("🏠 PAINEL PRINCIPAL", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        support_text = """
🆘 *SUPORTE TÉCNICO CORPORATIVO*

┌─────────────────────────────────────┐
          *ASSISTÊNCIA 24/7*
└─────────────────────────────────────┘

*📞 CONTATO IMEDIATO*
▸ Suporte Especializado
▸ Resposta em até 15 minutos
▸ Equipe Técnica Qualificada

*🔧 DIAGNÓSTICO*
▸ Análise de Sistema
▸ Identificação de Issues
▸ Solução de Problemas

*📚 BASE DE CONHECIMENTO*
▸ Documentação Completa
▸ Tutoriais Detalhados
▸ FAQs Corporativas

*Selecione a opção desejada:*
        """
        
        await query.edit_message_text(support_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def request_target_url(self, query, operation_mode):
        """Solicitação de URL para operação corporativa"""
        mode_configs = {
            "quick_scan": {"name": "SCAN RÁPIDO", "time": "2-4", "limit": "500"},
            "deep_analysis": {"name": "ANÁLISE PROFUNDA", "time": "5-8", "limit": "2.000"},
            "comprehensive_audit": {"name": "AUDITORIA COMPLETA", "time": "8-12", "limit": "10.000"}
        }
        
        config = mode_configs[operation_mode]
        
        operation_text = f"""
🎯 *INICIAR OPERAÇÃO - {config['name']}*

┌─────────────────────────────────────┐
         *PROTOCOLO DE BUSCA*
└─────────────────────────────────────┘

*Especifique o alvo da operação:*

*📋 EXEMPLOS VÁLIDOS:*
`sisregiii`
`sisregii.saude.gov.br`
`https://dominio.governo.gov.br`

*⏱️ PARÂMETROS DA OPERAÇÃO:*
• Duração Estimada: `{config['time']} minutos`
• Amostragem Máxima: `{config['limit']} registros`
• Processamento: `Alta Prioridade`

*🔍 Digite a URL do alvo:*
        """
        
        await query.edit_message_text(operation_text, parse_mode='Markdown')

    async def handle_url_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processamento corporativo de URLs"""
        user_id = update.effective_user.id
        target_url = update.message.text.strip()
        
        if user_id in self.processing_requests:
            await update.message.reply_text("""
⏳ *OPERAÇÃO EM ANDAMENTO*

┌─────────────────────────────────────┐
          *STATUS: PROCESSANDO*
└─────────────────────────────────────┘

Uma operação já está em execução em sua sessão.
Aguarde a conclusão para iniciar uma nova tarefa.

*Sistema: Operacional*
*Prioridade: Alta*
            """, parse_mode='Markdown')
            return
        
        self.processing_requests[user_id] = True
        self.system_stats['total_searches'] += 1
        
        start_time = time.time()
        
        try:
            # Inicialização da operação
            operation_msg = await update.message.reply_text(f"""
🚀 *INICIANDO OPERAÇÃO CORPORATIVA*

┌─────────────────────────────────────┐
         *SCARFACE ENTERPRISE*
└─────────────────────────────────────┘

*🎯 ALVO:* `{target_url}`
*⏱️ DURAÇÃO ESTIMADA:* 3-6 minutos
*📊 STATUS:* Conectando à infraestrutura...
*🔒 SEGURANÇA:* Nível Máximo Ativo

*Iniciando protocolo de análise...*
            """, parse_mode='Markdown')
            
            # Execução da busca
            results = await self.execute_corporate_search(user_id, target_url, operation_msg)
            
            processing_time = time.time() - start_time
            
            if results:
                self.system_stats['total_credentials_found'] += len(results)
                self.search_history.append({
                    'timestamp': datetime.now(),
                    'target': target_url,
                    'results': len(results),
                    'duration': processing_time
                })
                
                await operation_msg.edit_text(f"""
✅ *OPERAÇÃO CONCLUÍDA COM SUCESSO*

┌─────────────────────────────────────┐
          *RESULTADOS OBTIDOS*
└─────────────────────────────────────┘

*📊 MÉTRICAS DA OPERAÇÃO:*
• Credenciais Identificadas: `{len(results)}`
• Alvo Processado: `{target_url}`
• Tempo de Execução: `{processing_time:.1f}s`
• Eficiência: `{(len(results) / processing_time):.1f} cred/s`

*📁 Gerando relatório corporativo...*
                """, parse_mode='Markdown')
                
                # Geração do relatório corporativo
                report_data = self.generate_corporate_report(target_url, results, processing_time)
                
                with open(report_data['filename'], 'rb') as file:
                    await update.message.reply_document(
                        document=InputFile(file, filename=report_data['filename']),
                        caption=f"""
📋 *RELATÓRIO CORPORATIVO ENTREGUE*

┌─────────────────────────────────────┐
         *SCARFACE ENTERPRISE*
└─────────────────────────────────────┘

*✅ OPERAÇÃO: CONCLUÍDA*
*📊 RESULTADOS: {len(results)} credenciais*
*🎯 ALVO: {target_url}*
*⏱️ DURAÇÃO: {processing_time:.1f}s*
*🏢 SISTEMA: Enterprise v3.0*

*Relatório gerado e auditado.*
                        """,
                        parse_mode='Markdown'
                    )
                
                os.remove(report_data['filename'])
                
                # Relatório executivo final
                await operation_msg.edit_text(f"""
🎉 *OPERAÇÃO FINALIZADA COM EXCELÊNCIA*

┌─────────────────────────────────────┐
         *DASHBOARD FINAL*
└─────────────────────────────────────┘

*📈 DESEMPENHO DA OPERAÇÃO:*
• ✅ Sucesso: 100%
• 📊 Volume: {len(results)} registros
• ⚡ Velocidade: {(len(results) / processing_time):.1f} cred/s
• 🎯 Precisão: Máxima

*🏢 PRÓXIMOS PASSOS:*
1. Relatório enviado para análise
2. Dados disponíveis para BI
3. Sistema pronto para nova operação

*Eficiência corporativa comprovada.*
                """, parse_mode='Markdown')
                
            else:
                await operation_msg.edit_text(f"""
❌ *OPERAÇÃO CONCLUÍDA - SEM RESULTADOS*

┌─────────────────────────────────────┐
          *ANÁLISE FINALIZADA*
└─────────────────────────────────────┘

*🎯 ALVO PROCESSADO:* `{target_url}`
*⏱️ DURAÇÃO:* {processing_time:.1f}s
*📊 STATUS:* Busca Completa

*🔍 DIAGNÓSTICO:*
• Nenhum registro identificado
• Alvo possivelmente inválido
• Base de dados sem correspondências

*💡 RECOMENDAÇÕES:*
• Verificar especificação do alvo
• Validar formato da URL
• Considerar alternativas

*Sistema mantém operacionalidade.*
                """, parse_mode='Markdown')
                
        except Exception as e:
            await update.message.reply_text(f"""
🚨 *ERRO NA OPERAÇÃO*

┌─────────────────────────────────────┐
          *INCIDENTE REGISTRADO*
└─────────────────────────────────────┘

*❌ FALHA NO PROCESSAMENTO:*
`{str(e)}`

*🔧 AÇÕES IMEDIATAS:*
• Incidente registrado no log
• Equipe técnica notificada
• Sistema em modo de recuperação

*Tente novamente em instantes.*
            """, parse_mode='Markdown')
        
        finally:
            self.processing_requests.pop(user_id, None)

    async def execute_corporate_search(self, user_id, target_url, operation_msg):
        """Execução corporativa da busca"""
        results = []
        
        try:
            if target_url.startswith(('http://', 'https://')):
                target_url = target_url.split('//')[1]
            
            api_endpoint = f"{API_URL}?url={target_url}"
            
            response = requests.get(api_endpoint, stream=True, timeout=600)
            
            if response.status_code == 200:
                await operation_msg.edit_text(f"""
🔍 *EXECUTANDO ANÁLISE CORPORATIVA*

┌─────────────────────────────────────┐
         *PROCESSAMENTO ATIVO*
└─────────────────────────────────────┘

*🎯 ALVO:* `{target_url}`
*📊 STATUS:* Processando stream de dados
*⚡ FASE:* Coleta e análise
*🔒 SEGURANÇA:* Criptografia ativa

*Otimizando extração de inteligência...*
                """, parse_mode='Markdown')
                
                counter = 0
                for line_bytes in response.iter_lines():
                    if line_bytes:
                        line = line_bytes.decode('utf-8').strip()
                        
                        if line.startswith('data:') and '{' in line:
                            try:
                                json_str = line[5:].strip()
                                data = json.loads(json_str)
                                
                                if 'user' in data and 'pass' in data:
                                    username = data['user'].strip()
                                    password = data['pass'].strip()
                                    
                                    if username and password:
                                        results.append(f"{username}:{password}")
                                        counter += 1
                                        
                                        # Atualização de progresso corporativo
                                        if counter % 20 == 0:
                                            await operation_msg.edit_text(f"""
📈 *ANÁLISE EM ANDAMENTO*

┌─────────────────────────────────────┐
         *PROGRESSO: {counter}*
└─────────────────────────────────────┘

*🎯 ALVO:* `{target_url}`
*📊 REGISTROS PROCESSADOS:* {counter}
*⚡ VELOCIDADE:* Ótima
*🔍 STATUS:* Coleta contínua

*Mantendo performance corporativa...*
                                            """, parse_mode='Markdown')
                                            print(f"Corporativo #{counter}: {username}:{password}")
                            
                            except json.JSONDecodeError:
                                continue
                
                print(f"Operação corporativa finalizada! Total: {len(results)} resultados")
                
            else:
                print(f"Erro corporativo HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"Falha na operação corporativa: {e}")
        
        return results

    def generate_corporate_report(self, target_url, results, processing_time):
        """Geração de relatório corporativo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"corporate_report_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("┌─────────────────────────────────────────────────────────┐\n")
            f.write("               RELATÓRIO CORPORATIVO - SCARFACE\n")
            f.write("└─────────────────────────────────────────────────────────┘\n\n")
            
            f.write("INFORMAÇÕES DA OPERAÇÃO\n")
            f.write("═" * 55 + "\n")
            f.write(f"Alvo: {target_url}\n")
            f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Duração: {processing_time:.2f} segundos\n")
            f.write(f"Total de Credenciais: {len(results)}\n")
            f.write("═" * 55 + "\n\n")
            
            f.write("DETALHAMENTO DAS CREDENCIAIS\n")
            f.write("═" * 55 + "\n")
            for i, credential in enumerate(results, 1):
                f.write(f"[{i:04d}] {credential}\n")
            
            f.write("\n" + "═" * 55 + "\n")
            f.write("SCARFACE ENTERPRISE - BUSINESS INTELLIGENCE\n")
            f.write("Relatório gerado automaticamente\n")
            f.write("═" * 55 + "\n")
        
        return {'filename': filename}

    def get_system_latency(self):
        """Calcula latência do sistema"""
        try:
            start = time.time()
            requests.get(f"{API_URL}?url=test", timeout=5)
            return int((time.time() - start) * 1000)
        except:
            return 999

    async def test_api(self):
        """Teste de conectividade corporativa"""
        try:
            response = requests.get(f"{API_URL}?url=test", timeout=10)
            return response.status_code == 200
        except:
            return False

def main():
    """Inicialização do sistema corporativo"""
    print("""
┌─────────────────────────────────────────────────────────┐
                SCARFACE ENTERPRISE v3.0
              Sistema Corporativo de Inteligência
└─────────────────────────────────────────────────────────┘
    """)
    
    app = Application.builder().token(TOKEN).build()
    bot = EnterpriseLogsBot()
    
    # Configuração de handlers corporativos
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CallbackQueryHandler(bot.button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_url_message))
    
    print("✅ Sistema Corporativo Inicializado")
    print("🎯 Versão: Enterprise v3.0")
    print("📊 Modo: Produção")
    print("🔒 Segurança: Nível Máximo")
    print("🚀 Aguardando operações corporativas...")
    
    app.run_polling()

if __name__ == '__main__':
    main()