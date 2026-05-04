# GUI/CustomComboBox.py
from PySide6.QtWidgets import QComboBox, QMessageBox
from PySide6.QtCore import Signal

class AddableComboBox(QComboBox):
    """QComboBox с возможностью добавления нового элемента"""
    
    item_added = Signal(object)  # Сигнал о добавлении нового элемента
    
    def __init__(self, parent=None, data_loader=None, model_type=None, field_type=None):
        """
        model_type: 'engine', 'gear', 'encoder'
        field_type: 'company' или 'type'
        """
        super().__init__(parent)
        self.data_loader = data_loader
        self.model_type = model_type
        self.field_type = field_type
        
        # Загружаем существующие элементы
        self._refresh_items()
        
        # Подключаем сигнал изменения индекса
        self.currentIndexChanged.connect(self._on_index_changed)
    
    def _on_index_changed(self, index):
        """Обработка выбора пункта 'Добавить новый...'"""
        # Проверяем, выбран ли пункт "Добавить новый..."
        if index >= 0 and self.itemData(index) is None:
            # Открываем диалог добавления
            from GUI.TableWindow import AddItemDialog
            dialog = AddItemDialog(self.field_type, self)
            
            if dialog.exec() == AddItemDialog.Accepted:
                result = dialog.get_result()
                if result:
                    try:
                        # Добавляем в БД
                        new_item = self._add_to_database(result)
                        if new_item:
                            # Обновляем список
                            self._refresh_items()
                            # Выбираем новый элемент
                            for i in range(self.count()):
                                if self.itemData(i) == new_item[0]:
                                    self.setCurrentIndex(i)
                                    break
                            # Испускаем сигнал
                            self.item_added.emit(new_item)
                    except Exception as e:
                        QMessageBox.critical(self, "Ошибка", f"Не удалось добавить: {str(e)}")
            
            # Возвращаемся на первый элемент, если добавлять отменили
            if self.count() > 0 and self.currentIndex() == index:
                self.setCurrentIndex(0)
    
    def _add_to_database(self, data):
        """Добавляет новый элемент в БД"""
        try:
            if self.model_type == 'engine':
                if self.field_type == 'company':
                    return self.data_loader.add_engine_company(data['name'], data.get('country'))
                else:  # type
                    return self.data_loader.add_engine_type(data['name'])
            
            elif self.model_type == 'gear':
                if self.field_type == 'company':
                    return self.data_loader.add_gear_company(data['name'], data.get('country'))
                else:  # type
                    return self.data_loader.add_gear_type(data['name'])
            
            elif self.model_type == 'encoder':
                if self.field_type == 'company':
                    return self.data_loader.add_encoder_company(data['name'], data.get('country'))
                else:  # type
                    return self.data_loader.add_encoder_type(data['name'])
        except Exception as e:
            print(f"Ошибка при добавлении в БД: {e}")
            raise e
        
        return None
    
    def _refresh_items(self):
        """Обновляет список элементов"""
        # Блокируем сигналы, чтобы не вызывать лишние обновления
        self.blockSignals(True)
        
        # Сохраняем текущий выбранный элемент
        current_data = self.currentData()
        
        # Очищаем список
        self.clear()
        
        # Загружаем свежие данные
        items = self._load_items()
        
        # Добавляем существующие элементы
        if items:
            for item_id, item_name in items:
                self.addItem(item_name, item_id)
        else:
            # Если нет элементов, показываем сообщение
            self.addItem("Нет доступных опций", None)
        
        # Добавляем опцию добавления нового
        self.addItem("➕ Добавить новый...", None)
        
        # Восстанавливаем выбранный элемент, если он был
        if current_data is not None:
            for i in range(self.count()):
                if self.itemData(i) == current_data:
                    self.setCurrentIndex(i)
                    break
        elif self.count() > 0:
            # Если ничего не выбрано, выбираем первый элемент (если это не "Добавить новый")
            if self.itemData(0) is not None:
                self.setCurrentIndex(0)
        
        # Разблокируем сигналы
        self.blockSignals(False)
    
    def _load_items(self):
        """Загружает элементы из БД"""
        try:
            if self.model_type == 'engine':
                if self.field_type == 'company':
                    return self.data_loader.get_engine_companies()
                else:
                    return self.data_loader.get_engine_types()
            
            elif self.model_type == 'gear':
                if self.field_type == 'company':
                    return self.data_loader.get_gear_companies()
                else:
                    return self.data_loader.get_gear_types()
            
            elif self.model_type == 'encoder':
                if self.field_type == 'company':
                    return self.data_loader.get_encoder_companies()
                else:
                    return self.data_loader.get_encoder_types()
        except Exception as e:
            print(f"Ошибка при загрузке элементов: {e}")
        
        return []