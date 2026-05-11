from PySide6.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QMessageBox, QDialog, QFormLayout,
                               QLineEdit, QDialogButtonBox, QScrollArea, 
                               QSpinBox, QDoubleSpinBox, QFileDialog)
from .DBModelGUI import SQLAlchemyTableModel
from DataBase.ORMModel import CoefRegulators, EngineDC, Encoder, Gear, Result, SourceData, Utils
from DataBase.repository import DatabaseRepository
from typing import Type
from sqlalchemy.orm import DeclarativeBase
import os


from typing import Type
from sqlalchemy.orm import DeclarativeBase
from utils.column_mapping_loader import load_column_mapping
from utils.data_loader import DataLoader
from GUI.CustomComboBox import AddableComboBox
from GUI.ResultShowWindow import ResultShowWindow
from GUI.RecordDetailWindow import RecordDetailWindow
from GUI import html_func
from utils.SourData import SourceDataDriver, DataDriver, DataGear, DataEncoder
from GUI.RecordDetailWindow import RecordDetailWindow
from GUI import html_func


class FilePickerWidget(QWidget):
    """Виджет для выбора файла чертежа с кнопкой"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Поле для отображения пути
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Выберите файл чертежа")
        self.path_input.setReadOnly(True)
        
        # Кнопка для открытия диалога
        self.browse_button = QPushButton("Обзор...")
        self.browse_button.setMaximumWidth(100)
        self.browse_button.clicked.connect(self._on_browse)
        
        layout.addWidget(self.path_input)
        layout.addWidget(self.browse_button)
        self.setLayout(layout)
    
    def _on_browse(self):
        """Открывает диалог выбора файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите чертеж",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.pdf);;Все файлы (*.*)"
        )
        if file_path:
            # Преобразуем абсолютный путь в относительный
            try:
                # Получаем текущую рабочую директорию проекта
                project_root = os.getcwd()
                relative_path = os.path.relpath(file_path, project_root)
                self.path_input.setText(relative_path)
            except ValueError:
                # Если не удалось создать относительный путь, используем абсолютный
                self.path_input.setText(file_path)
    
    def set_value(self, value):
        """Устанавливает путь к файлу"""
        if value:
            self.path_input.setText(str(value))
        else:
            self.path_input.clear()
    
    def get_value(self):
        """Получает путь к файлу"""
        path = self.path_input.text().strip()
        return path if path else None


class TableWindow(QWidget):
    def __init__(self, ORMModel: Type[DeclarativeBase]):
        super().__init__()
        self.setWindowTitle("База данных PostgreSQL")
        self.setGeometry(100, 100, 1000, 600)
        
        # Создаем репозиторий
        self.repository = DatabaseRepository() 
        
        self.table = QTableView()
        self.ORM_Model = ORMModel
        self.current_data = [] 
        
        # Создаем кнопки
        self.open_button = QPushButton("Открыть")
        self.refresh_button = QPushButton("Обновить")
        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        
        
        # Создаем горизонтальный layout для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        
        # Основной layout (вертикальный)
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        # Подключаем сигналы
        self.open_button.clicked.connect(self.open_record)
        self.refresh_button.clicked.connect(self.load_data)
        self.add_button.clicked.connect(self.add_record)
        self.edit_button.clicked.connect(self.edit_record)
        self.delete_button.clicked.connect(self.delete_record)
        
        # Загружаем данные
        self.load_data()
    
    def get_selected_record_id(self):
        """Получает ID выбранной записи"""
        selection = self.table.selectionModel()
        if selection.hasSelection():
            selected_indexes = selection.selectedRows()
            if selected_indexes:
                row = selected_indexes[0].row()
                if row < len(self.current_data):
                    record = self.current_data[row]
                    # Получаем ID из словаря или объекта
                    if isinstance(record, dict):
                        return record.get('id')
                    else:
                        return record.id
        return None
    
    def open_record(self):
        """Открывает подробности выбранной записи"""
        record_id = self.get_selected_record_id()
        
        if record_id is None:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для открытия")
            return
        
        try:
            record = self.repository.get_first_data_by_id_with_relations(self.ORM_Model, record_id)
            
            if not record:
                QMessageBox.warning(self, "Ошибка", f"Запись с ID {record_id} не найдена")
                return
            
            # Для таблицы Result используем специальное окно
            if self.ORM_Model == Result:
                self.result_window = ResultShowWindow(
                    motor=record.engine_rel,
                    source_data=record.source_data_rel,
                    gear=record.gear_rel,
                    closest_encoder=record.encoder_rel,
                    coef_regulators=record.coef_regulators_rel,
                    utils=record.utils_rel
                )
                self.result_window.show()
            
            # SourceData
            elif self.ORM_Model == SourceData:
                source_data_obj = SourceDataDriver(
                    max_angl_speed=getattr(record, 'max_speed', 0),
                    max_angle_speed_wm=getattr(record, 'max_speed_work', 0),
                    max_angle_acc_wm=getattr(record, 'max_acc', 0),
                    tp=getattr(record, 'acc_duration', 0),
                    tp_rel=getattr(record, 'rel_duration', 0),
                    max_stat_torque=getattr(record, 'max_torque', 0),
                    eq_torque_intertia=getattr(record, 'max_inertia_torque', 0),
                    max_error=getattr(record, 'max_error', 0),
                    overshoot=getattr(record, 'overshoot', 0),
                    transition_time=getattr(record, 'transition_time', 0)
                )
                html = html_func.html_source_data(source_data_obj)
                self.detail_window = RecordDetailWindow("Исходные данные", html)
                self.detail_window.show()
            
            # EngineDC (двигатель)
            elif self.ORM_Model == EngineDC:
                motor_obj = DataDriver(
                    id=getattr(record, 'id', 0),
                    name=getattr(record, 'model', ''),
                    p_nom=getattr(record, 'p_nom', 0),
                    torque_nom=getattr(record, 'm_nom', 0),
                    n_nom=getattr(record, 'n_nom', 0),
                    U_nom=getattr(record, 'u_nom', 0),
                    I_nom=getattr(record, 'i_nom', 0),
                    R=getattr(record, 'r_nom', 0),
                    J=getattr(record, 'j_nom', 0),
                    m=getattr(record, 'm', 0),
                    L_a=getattr(record, 'l_a', 0),
                    max_current=getattr(record, 'max_current', getattr(record, 'i_nom', 0) * 5),
                    drawing=getattr(record, 'drawing', None)
                )
                html = html_func.html_found_motor(motor_obj)
                self.detail_window = RecordDetailWindow("Двигатель", html)
                self.detail_window.show()
            
            # Gear (редуктор)
            elif self.ORM_Model == Gear:
                gear_obj = DataGear(
                    id=getattr(record, 'id', 0),
                    name=getattr(record, 'gear_name', ''),
                    i_nom=getattr(record, 'i', 0),
                    m=getattr(record, 'mass', 0),
                    kpd=getattr(record, 'efficiency', 0),
                    c=getattr(record, 'c', 0),
                    clearance=getattr(record, 'clearance', 0),
                    speed_norm=getattr(record, 'speed_norm', 0),
                    torque_nom=getattr(record, 'torque_nom', 0),
                    efficiency=getattr(record, 'efficiency', 0),
                    drawing=getattr(record, 'drawing', None)
                )
                html = html_func.html_found_gear(gear_obj)
                self.detail_window = RecordDetailWindow("Редуктор", html)
                self.detail_window.show()
            
            # Encoder (энкодер)
            elif self.ORM_Model == Encoder:
                encoder_obj = DataEncoder(
                    id=getattr(record, 'id', 0),
                    name=getattr(record, 'encoder_name', ''),
                    m=getattr(record, 'weight', 0),
                    j=getattr(record, 'rotor_moment_of_inertia', 0),
                    max_speed=getattr(record, 'maximum_rotation_speed', 0),
                    N=getattr(record, 'lines_count', 0),
                    #type=getattr(record, 'type', ''),
                    drawing=getattr(record, 'drawing', None)
                )
                html = html_func.html_found_encoder(encoder_obj)
                self.detail_window = RecordDetailWindow("Энкодер", html)
                self.detail_window.show()
            
            # CoefRegulators (коэффициенты)
            elif self.ORM_Model == CoefRegulators:
                html = html_func.html_coef_regulators(record)
                self.detail_window = RecordDetailWindow("Коэффициенты регуляторов", html)
                self.detail_window.show()
            
            # Utils (утилиты)
            elif self.ORM_Model == Utils:
                html = html_func.html_utils_data(record)
                self.detail_window = RecordDetailWindow("Утилиты", html)
                self.detail_window.show()
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть запись:\n{str(e)}")
    
    def load_data(self):
        """Загружает данные из БД через репозиторий"""
        try:
            orm_model = self.ORM_Model
            
            # Получаем данные через репозиторий
            data = self.repository.get_data_with_relations(orm_model)
            self.current_data = data
            
            # Получаем колонки
            columns = [col.name for col in orm_model.__table__.columns]
            # Создаем модель для таблицы, передавая класс модели
            model = SQLAlchemyTableModel(data, columns, model_class=orm_model) 
            self.table.setModel(model)
            
            # Настраиваем выделение строк
            self.table.setSelectionBehavior(QTableView.SelectRows)
            
            # Настраиваем ширину колонок
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные:\n{str(e)}")
    
    def add_record(self):
        """Добавление новой записи"""
        dialog = RecordDialog(self.ORM_Model, record=None, parent=self)
        
        if dialog.exec() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                print(f"Добавление записи с данными: {data}")
                
                # Используем метод add из репозитория
                self.repository.add(self.ORM_Model, data)
                
                QMessageBox.information(self, "Успех", "Запись успешно добавлена")
                self.load_data()  # Обновляем таблицу
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запись:\n{str(e)}")
    
    def edit_record(self):
        """Редактирование выбранной записи"""
        record_id = self.get_selected_record_id()
        
        if record_id is None:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для редактирования")
            return
        
        try:
            # Получаем текущие данные записи
            current_record = None
            for record in self.current_data:
                if isinstance(record, dict):
                    if record.get('id') == record_id:
                        current_record = record
                        break
                else:
                    if record.id == record_id:
                        current_record = record
                        break
            
            dialog = RecordDialog(self.ORM_Model, record=current_record, parent=self)
            
            if dialog.exec() == QDialog.Accepted:
                data = dialog.get_data()
                print(f"Обновление записи {record_id} с данными: {data}")
                
                # Используем метод update из репозитория
                self.repository.update(self.ORM_Model, record_id, data)
                
                QMessageBox.information(self, "Успех", "Запись успешно обновлена")
                self.load_data()  # Обновляем таблицу
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить запись:\n{str(e)}")
    
    def delete_record(self):
        """Удаление выбранной записи"""
        record_id = self.get_selected_record_id()
        
        if record_id is None:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для удаления")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", 
                                    "Вы уверены, что хотите удалить эту запись?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # Используем метод delete из репозитория
                self.repository.delete(self.ORM_Model, record_id)
                
                QMessageBox.information(self, "Успех", "Запись успешно удалена")
                self.load_data()  # Обновляем таблицу
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить запись:\n{str(e)}")

class RecordDialog(QDialog):
    """Диалоговое окно для добавления/редактирования записи"""
    
    def __init__(self, orm_model, record=None, parent=None):
        super().__init__(parent)
        self.orm_model = orm_model
        self.record = record
        self.inputs = {}
        self.data_loader = DataLoader()
        
        # Загружаем маппинг из YAML
        self.column_mapping = load_column_mapping(orm_model)
        
        self.setWindowTitle("Добавление записи" if record is None else "Редактирование записи")
        self.setModal(True)
        self.resize(600, 500)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Получаем колонки модели
        for column in orm_model.__table__.columns:
            # Пропускаем первичный ключ (id)
            if column.primary_key:
                continue
            
            # Получаем русское название из маппинга
            field_label = self.column_mapping.get(column.name, column.name)
            
            # Создаем поле ввода
            input_field = self._create_input_field(column)
            
            # Если редактируем, заполняем текущими значениями
            if record:
                self._set_field_value(input_field, column.name)
            
            form_layout.addRow(f"{field_label}:", input_field)
            self.inputs[column.name] = input_field
        
        # Добавляем скролл
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # Кнопки OK/Cancel
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def _create_input_field(self, column):
        """Создает поле ввода в зависимости от типа"""
        column_name = column.name
        column_type = str(column.type).lower()
        
        # Для выбора файла чертежа
        if column_name == 'drawing':
            return FilePickerWidget(parent=self)
        
        # Определяем, является ли поле внешним ключом
        is_foreign_key = column_name in ['company', 'type_id', 'gear_company', 
                                        'gear_type', 'id_company', 'id_type_encoder']
        
        # Для внешних ключей создаем AddableComboBox
        if is_foreign_key:
            model_type = self._get_model_type()
            field_type = self._get_field_type(column_name)
            
            combobox = AddableComboBox(
                parent=self,
                data_loader=self.data_loader,
                model_type=model_type,
                field_type=field_type
            )
            return combobox
        
        # Для числовых полей
        elif 'int' in column_type:
            spinbox = QSpinBox()
            spinbox.setMinimum(-999999)
            spinbox.setMaximum(999999)
            spinbox.setMaximumWidth(200)
            return spinbox
        
        elif 'float' in column_type or 'numeric' in column_type:
            spinbox = QDoubleSpinBox()
            spinbox.setMinimum(-999999.99)
            spinbox.setMaximum(999999.99)
            spinbox.setDecimals(6)
            spinbox.setMaximumWidth(200)
            return spinbox
        
        # Для текстовых полей
        else:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Введите значение")
            return line_edit
    
    def _get_model_type(self):
        """Определяет тип модели (engine, gear, encoder)"""
        if self.orm_model == EngineDC:
            return 'engine'
        elif self.orm_model == Gear:
            return 'gear'
        elif self.orm_model == Encoder:
            return 'encoder'
        return None
    
    def _get_field_type(self, column_name):
        """Определяет тип поля (company или type)"""
        if 'company' in column_name:
            return 'company'
        else:
            return 'type'
    
    def _set_field_value(self, input_field, field_name):
        """Устанавливает значение поля при редактировании"""
        if isinstance(self.record, dict):
            value = self.record.get(field_name, "")
        else:
            value = getattr(self.record, field_name, "")
        
        if isinstance(input_field, FilePickerWidget):
            input_field.set_value(value)
        elif isinstance(input_field, AddableComboBox):
            # Ищем элемент с соответствующим ID
            for i in range(input_field.count()):
                if input_field.itemData(i) == value:
                    input_field.setCurrentIndex(i)
                    break
        elif isinstance(input_field, QSpinBox):
            input_field.setValue(int(value) if value else 0)
        elif isinstance(input_field, QDoubleSpinBox):
            input_field.setValue(float(value) if value else 0.0)
        else:
            input_field.setText(str(value) if value else "")
    
    def get_data(self):
        """Получает данные из формы"""
        data = {}
        for field_name, input_field in self.inputs.items():
            if isinstance(input_field, FilePickerWidget):
                value = input_field.get_value()
                if value is not None:
                    data[field_name] = value
            elif isinstance(input_field, AddableComboBox):
                value = input_field.currentData()
                if value is not None:
                    data[field_name] = value
            elif isinstance(input_field, QSpinBox):
                data[field_name] = input_field.value()
            elif isinstance(input_field, QDoubleSpinBox):
                data[field_name] = input_field.value()
            else:
                value = input_field.text().strip()
                if value:
                    data[field_name] = value
        return data
    
class AddItemDialog(QDialog):
    """Диалог для добавления новой компании или типа"""
    
    def __init__(self, item_type, parent=None):
        """
        item_type: 'company' или 'type'
        """
        super().__init__(parent)
        self.item_type = item_type
        self.result_data = None
        
        self.setWindowTitle(f"Добавление {self._get_title()}")
        self.setModal(True)
        self.resize(400, 200)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Создаем поля ввода
        if item_type == 'company':
            self.name_input = QLineEdit()
            self.country_input = QLineEdit()
            form_layout.addRow("Название компании:", self.name_input)
            form_layout.addRow("Страна:", self.country_input)
        elif item_type == 'type':
            self.name_input = QLineEdit()
            form_layout.addRow("Название типа:", self.name_input)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def _get_title(self):
        """Возвращает заголовок окна"""
        if self.item_type == 'company':
            return "компании"
        else:
            return "типа"
    
    def _on_accept(self):
        """Обработка нажатия OK"""
        if self.item_type == 'company':
            name = self.name_input.text().strip()
            country = self.country_input.text().strip()
            
            if not name:
                QMessageBox.warning(self, "Ошибка", "Название компании обязательно!")
                return
            
            self.result_data = {
                'name': name,
                'country': country if country else None
            }
        else:  # type
            name = self.name_input.text().strip()
            if not name:
                QMessageBox.warning(self, "Ошибка", "Название типа обязательно!")
                return
            
            self.result_data = {
                'name': name
            }
        
        self.accept()
    
    def get_result(self):
        """Возвращает введенные данные"""
        return self.result_data